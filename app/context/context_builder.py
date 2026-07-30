class ContextBuilder:
    """
    Expands the retrieved tables by adding related tables using
    foreign-key relationships.

    This provides the LLM with enough schema context to generate
    correct JOIN queries.
    """

    def expand(
        self,
        retrieval_results,
        documents,
        top_k=3,
        max_depth=1
    ):
        """
        Expand retrieved tables with related tables.

        Parameters
        retrieval_results : list
            Ranked retrieval results.

        documents : list
            All indexed retrieval documents.

        top_k : int
            Number of top retrieved tables to expand.

        Returns
        list
            Expanded list of retrieval documents.
        """

        
        # Build lookup
    
        document_lookup = {}

        for document in documents:
            document_lookup[document["table"]] = document

        
        # Add top retrieved documents first
        
        expanded_documents = []

        selected_tables = set()

        for result in retrieval_results[:top_k]:

            table = result["table"]

            selected_tables.add(table)

            expanded_documents.append(
                result["document"]
            )

        
        for _ in range(max_depth):
            previous_count = len(selected_tables)

            self.expand_parent_tables(
                expanded_documents,
                selected_tables,
                document_lookup
            )

            self.expand_child_tables(
                expanded_documents,
                selected_tables,
                documents
            )

            if len(selected_tables) == previous_count:
                break

        return expanded_documents
 
    def expand_parent_tables(
        self,
        expanded_documents,
        selected_tables,
        document_lookup
    ):
        """
        Add tables referenced through foreign keys.

        Example:

        orders
            customer_id
                ↓
            customers
        """

        current_documents = list(expanded_documents)

        for document in current_documents:

            schema = document["structured"]

            for fk in schema["foreign_keys"]:

                referenced_table = (
                    fk["references"]["table"]
                )

                if referenced_table in selected_tables:
                    continue

                if referenced_table not in document_lookup:
                    continue

                selected_tables.add(
                    referenced_table
                )

                expanded_documents.append(
                    document_lookup[referenced_table]
                )

    def expand_child_tables(
        self,
        expanded_documents,
        selected_tables,
        documents
    ):
        """
        Add tables that reference already selected tables.

        Example:

        products

        ↑

        order_items.product_id
        """

        current_tables = list(selected_tables)

        for document in documents:

            table_name = document["table"]

            if table_name in selected_tables:
                continue

            schema = document["structured"]

            should_add = False

            for fk in schema["foreign_keys"]:

                parent = fk["references"]["table"]

                if parent in current_tables:

                    should_add = True
                    break

            if should_add:

                selected_tables.add(table_name)

                expanded_documents.append(document)
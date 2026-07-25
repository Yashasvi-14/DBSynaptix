from app.ai.provider import AIProvider


class SQLGenerator:
    """
    Generates SQL using the LLM.
    """

    def __init__(self):

        self.provider = AIProvider()

    def generate(
        self,
        prompt
    ):
        """
        Generate SQL from a prompt.

        Parameters
        ----------
        prompt : str

        Returns
        -------
        str
        """

        sql = self.provider.generate_text(
            prompt
        )

        if sql is None:
            raise RuntimeError("LLM returned no response.")

        return sql.strip()
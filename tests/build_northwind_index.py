from app.config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)

from app.schemas.database import DatabaseConnectionRequest
from app.services.indexing_service import IndexingService


def main():

    request = DatabaseConnectionRequest(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        username=DB_USER,
        password=DB_PASSWORD
    )

    service = IndexingService()

    print("=" * 80)
    print("BUILDING DATABASE INDEX")
    print("=" * 80)

    documents = service.build_index(
        request
    )

    print("")
    print("=" * 80)
    print("INDEX BUILT SUCCESSFULLY")
    print("=" * 80)

    print(f"Indexed tables: {len(documents)}")
    print("Saved to: data/index.json")


if __name__ == "__main__":
    main()
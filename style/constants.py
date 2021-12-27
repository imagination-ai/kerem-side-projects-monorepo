import os
from pathlib import Path

BASE_PATH: Path = Path(os.getenv("APP_RESOURCE_DIR", Path(__file__).parents[1]))
# Constants for utils.world_languages
WORLD_LANG_FILENAME = "world-lang.json"
WORLD_LANG_PATH = BASE_PATH / "resources/"

# Constants for style.crawler, style.reader
GUTENBERG_BASE_URL = "http://aleph.gutenberg.org/"
FILE_PATH_BOOK_DS = BASE_PATH / "datasets/book_ds"
FILE_PATH_MOCK_DS = BASE_PATH / "datasets/mock_ds"

# Constants for utils.author_catalog
CATALOG_FILE_PATH = BASE_PATH / "resources" / "pg_catalog.csv"
LOG_FILE_PATH = BASE_PATH / "resources" / "log.txt"

# Constants for tests.style.crawler.test_crawler
TEST_DATA_FILENAME = BASE_PATH / "resources" / "test_page.html"

# Constants for style.train.classifier_trainer
MODEL_EXPORT_PATH = BASE_PATH / "models/"

# Constants for utils.author_catalog

FINAL_SELECTED_AUTHOR = (
    "Dostoyevsky, Fyodor, 1821-1881",
    "Tolstoy, Leo, graf, 1828-1910",
    "Shakespeare, William, 1564-1616",
    "Kafka, Franz, 1883-1924",
    "Carroll, Lewis, 1832-1898",
    "Fitzgerald, F. Scott (Francis Scott), 1896-1940",
    "Dickens, Charles, 1812-1870",
    "Melville, Herman, 1819-1891",
    "Flaubert, Gustave, 1821-1880",
    "Balzac, Honoré de, 1799-1850",
    "Gorky, Maksim, 1868-1936",
    "Hugo, Victor, 1802-1885",
    "Gogol, Nikolai Vasilevich, 1809-1852",
    "Verne, Jules, 1828-1905",
    "Dickinson, Emily, 1830-1886",
    "Stendhal, 1783-1842",
    "Zola, Émile, 1840-1902",
    "Daudet, Alphonse, 1840-1897",
    "Sand, George, 1804-1876",
    "Dumas, Alexandre, 1824-1895",
    "Austen, Jane, 1775-1817",
    "Eliot, George, 1819-1880",
    "Brontë, Emily, 1818-1848",
    "Swift, Jonathan, 1667-1745",
    "Conrad, Joseph, 1857-1924",
    "Woolf, Virginia, 1882-1941",
    "Wilde, Oscar, 1854-1900",
    "Kipling, Rudyard, 1865-1936",
    "Twain, Mark, 1835-1910",
    "Hawthorne, Nathaniel, 1804-1864",
    "Wharton, Edith, 1862-1937",
    "Lewis, Sinclair, 1885-1951",
    "London, Jack, 1876-1916",
)

SELECTED_AUTHORS = (
    "Dostoyevsky, Fyodor, 1821-1881",
    "Tolstoy, Leo, graf, 1828-1910",
)

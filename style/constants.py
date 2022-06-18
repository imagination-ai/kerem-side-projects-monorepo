import os
from pathlib import Path

BASE_PATH: Path = Path(os.getenv("APP_RESOURCE_DIR", Path(__file__).parents[1]))

# Constants for utils.world_languages
WORLD_LANG_FILENAME = "world-lang.json"
WORLD_LANG_PATH = BASE_PATH / "resources/"

# Constants for style.crawler, style.reader
GUTENBERG_BASE_URL = "http://aleph.gutenberg.org/"
FILE_PATH_BOOK_DS = BASE_PATH / "style-resources" / "datasets/book_ds"
FILE_PATH_MOCK_DS = BASE_PATH / "style-resources" / "datasets/mock_ds"
FIGURES_PATH = BASE_PATH / "style-resources" / "figures"

# Constants for utils.author_catalog
CATALOG_FILE_PATH = (
    BASE_PATH / "style-resources" / "resources" / "pg_catalog.csv"
)
LOG_FILE_PATH = BASE_PATH / "style-resources" / "resources" / "log.txt"

# Constants for tests.style.crawler.test_crawler
TEST_DATA_FILENAME = (
    BASE_PATH / "style-resources" / "resources" / "test_page.html"
)

# Constants for style.train.classifier_trainer
MODEL_EXPORT_PATH = BASE_PATH / "style-resources" / "models/"

# Constants for style.crate_dataset_for_automl
FILE_PATH_AUTOML_DS = BASE_PATH / "style-resources" / "datasets/automl_ds"

# Constants for utils.author_catalog

FINAL_SELECTED_AUTHORS = (
    "Alcott, Louisa May, 1832-1888",
    "Anthony, Susan B. (Susan Brownell), 1820-1906",
    "Austen, Jane, 1775-1817",
    "Balzac, Honoré de, 1799-1850",
    "Barrie, J. M. (James Matthew), 1860-1937",
    "Baum, L. Frank (Lyman Frank), 1856-1919",
    "Bierce, Ambrose, 1842-1914?",
    "Brontë, Charlotte, 1816-1855",
    "Brontë, Emily, 1818-1848",
    "Burnett, Frances Hodgson, 1849-1924",
    "Burroughs, Edgar Rice, 1875-1950",
    "Burton, Richard Francis, Sir, 1821-1890",
    "Butler, Samuel, 1835-1902",
    "Byron, George Gordon Byron, Baron, 1788-1824",
    "Carroll, Lewis, 1832-1898",
    "Cervantes Saavedra, Miguel de, 1547-1616",
    "Chambers, Robert W. (Robert William), 1865-1933",
    "Chekhov, Anton Pavlovich, 1860-1904",
    "Chesterton, G. K. (Gilbert Keith), 1874-1936",
    "Chopin, Kate, 1850-1904",
    "Christie, Agatha, 1890-1976",
    "Conrad, Joseph, 1857-1924",
    "Conrad, Joseph, 1857-1924",
    "Dante Alighieri, 1265-1321",
    "Daudet, Alphonse, 1840-1897",
    "Defoe, Daniel, 1661?-1731",
    "Dickens, Charles, 1812-1870",
    "Dickinson, Emily, 1830-1886",
    "Dostoyevsky, Fyodor, 1821-1881",
    "Douglass, Frederick, 1818-1895",
    "Doyle, Arthur Conan, 1859-1930",
    "Du Bois, W. E. B. (William Edward Burghardt), 1868-1963",
    "Dumas, Alexandre, 1824-1895",
    "Eliot, George, 1819-1880",
    "Fitzgerald, F. Scott (Francis Scott), 1896-1940",
    "Flaubert, Gustave, 1821-1880",
    "Foote, Mary Hallock, 1847-1938",
    "Gilman, Charlotte Perkins, 1860-1935",
    "Goethe, Johann Wolfgang von, 1749-1832",
    "Gogol, Nikolai Vasilevich, 1809-1852",
    "Gorky, Maksim, 1868-1936",
    "Hardy, Thomas, 1840-1928",
    "Hawthorne, Nathaniel, 1804-1864",
    "Hugo, Victor, 1802-1885",
    "Ibsen, Henrik, 1828-1906",
    "Joyce, James, 1882-1941",
    "Kafka, Franz, 1883-1924",
    "Kipling, Rudyard, 1865-1936",
    "Lang, Andrew, 1844-1912",
    "Lewis, Sinclair, 1885-1951",
    "London, Jack, 1876-1916",
    "Machiavelli, Niccolò, 1469-1527",
    "Maupassant, Guy de, 1850-1893",
    "Melville, Herman, 1819-1891",
    "Mill, John Stuart, 1806-1873",
    "Montgomery, L. M. (Lucy Maud), 1874-1942",
    "Nietzsche, Friedrich Wilhelm, 1844-1900",
    "Plato, 427? BCE-347? BCE",
    "Poe, Edgar Allan, 1809-1849",
    "Pope, Alexander, 1688-1744",
    "Potter, Beatrix, 1866-1943",
    "Russell, Bertrand, 1872-1970",
    "Sand, George, 1804-1876",
    "Scott, Walter, 1771-1832",
    "Shakespeare, William, 1564-1616",
    "Shaw, Bernard, 1856-1950",
    "Shelley, Mary Wollstonecraft, 1797-1851",
    "Stendhal, 1783-1842",
    "Stevenson, Robert Louis, 1850-1894",
    "Stoker, Bram, 1847-1912",
    "Swift, Jonathan, 1667-1745",
    "Thoreau, Henry David, 1817-1862",
    "Tolstoy, Leo, graf, 1828-1910",
    "Twain, Mark, 1835-1910",
    "Verne, Jules, 1828-1905",
    "Voltaire, 1694-1778",
    "Wells, H. G. (Herbert George), 1866-1946",
    "Wharton, Edith, 1862-1937",
    "Wilde, Oscar, 1854-1900",
    "Wittgenstein, Ludwig, 1889-1951",
    "Wodehouse, P. G. (Pelham Grenville), 1881-1975",
    "Woolf, Virginia, 1882-1941",
    "Zola, Émile, 1840-1902",
)

SELECTED_AUTHORS = (
    "Dostoyevsky, Fyodor, 1821-1881",
    "Tolstoy, Leo, graf, 1828-1910",
    "Jefferson, Thomas, 1743-1826",
)

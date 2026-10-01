import pickle
import sys
import os
from pympler import asizeof
import nltk
from nltk import PorterStemmer, WordNetLemmatizer


"""
import nltk
from nltk.corpus import reuters
from nltk.tokenize import word_tokenize
# download resources (only once)
nltk.download('reuters')
nltk.download('punkt')
nltk.download('punkt_tab')

data = []

for doc_id in reuters.fileids():
    text = reuters.raw(doc_id)          # get raw text
    tokens = word_tokenize(text)        # tokenize using NLTK
    data.append((doc_id, tokens))       # (doc_id, tokens)

with open("data.pkl", "wb") as f:
    pickle.dump(data, f)
"""


with open("data.pkl", "rb") as f:
    data = pickle.load(f)


# print('First document id', data[0][0])
# print('First document tokens', data[0][1])
# print('Total number of documents', len(data))


class Node():
    def __init__(self, term: str, DocID: str | None = None):
        self.left = None
        self.right = None
        self.data = {"term": term, "DocID": [DocID] if DocID else []}


def Insert(root: Node, term: str, DocID: str):
    if root is None:
        return Node(term, DocID)
    elif term < root.data["term"]:
        root.left = Insert(root.left, term, DocID)
    elif term > root.data["term"]:
        root.right = Insert(root.right, term, DocID)
    else:
        if DocID not in root.data["DocID"]:
            root.data["DocID"].append(DocID)
            root.data["DocID"].sort()
    return root


def Inorder(root: Node):
    if root:
        Inorder(root.left)
        print(f"term: {root.data["term"]}")
        print(f"DocIDs: {root.data["DocID"]}")
        Inorder(root.right)


def Removekey(root: Node, term: str):
    ptr = root
    while ptr != None:
        if ptr.data["term"] == term:
            break
        pre = ptr
        if term < ptr.data["term"]:
            ptr = ptr.left
        else:
            ptr = ptr.right

    if ptr == None:
        return root

    if ptr == root and ptr.right == None and ptr.left == None:
        root = None
        return root

    if ptr.right == None and ptr.left == None:
        if pre.data["term"] >= ptr.data["term"]:
            pre.left = None
        else:
            pre.right = None
        return root

    if ptr.right != None and ptr.left == None:
        if ptr == root:
            root = ptr.right
        elif pre.data["term"] >= ptr.data["term"]:
            pre.left = ptr.right
        else:
            pre.right = ptr.right
        return root

    if ptr.right == None and ptr.left != None:
        if ptr == root:
            root = ptr.left
        elif pre.data["term"] >= ptr.data['term']:
            pre.left = ptr.left
        else:
            pre.right = ptr.left
        return root

    if ptr.right != None and ptr.left != None:
        t = ptr.right
        while t.left != None:
            pre = t
            t = t.left
        ptr.data = t.data
        if t == ptr.right:
            ptr.right = t.right
        else:
            pre.left = t.right
        return root
    return root


def Search(root: Node, term: str):
    found_node = Search2(root, term)
    if found_node.data["term"] == " ":
        print("Query not found!")
    else:
        print(f"Query: {query}")
        print(f"Documents retrieved: {len(found_node.data["DocID"])}")
        sys.stdout.write(f"Doc IDs: [")
        for i in found_node.data["DocID"][:10]:
            sys.stdout.write(f"'{i}', ")
        sys.stdout.write("]")


def Search2(root: Node, term: str):
    if term > root.data["term"] and root.right != None:
        root = Search2(root.right, term)
    elif term < root.data["term"] and root.left != None:
        root = Search2(root.left, term)
    elif term == root.data["term"] and root != None:
        return root
    elif root.left == None or root.right == None:
        return Node(" ", " ")
    return root


def Search_with_AND(root: Node, term: str):
    found_node = Search_with_AND2(root, term)
    if found_node.data["term"] == " ":
        print("Query not found!")
    else:
        print(f"Query: {query}")
        print(f"Documents retrieved: {len(found_node.data["DocID"])}")
        sys.stdout.write(f"Doc IDs: [")
        for i in found_node.data["DocID"][:10]:
            sys.stdout.write(f"'{i}', ")
        sys.stdout.write("]")


def Search_with_AND2(root: Node, term: str):
    term = term.split()
    term1 = Search2(root, term[0])
    term2 = Search2(root, term[2])
    if term1.data["term"] == " " or term2.data["term"] == " ":
        return Node(" ", " ")
    i = 0
    j = 0
    t_INX = 0
    temp_list = []
    while True:
        if term1.data["DocID"][i] == term2.data["DocID"][j]:
            temp_list.append(term1.data["DocID"][i])
            i += 1
            j += 1
            t_INX += 1
        elif term1.data["DocID"][i] < term2.data["DocID"][j]:
            i += 1
        elif term1.data["DocID"][i] > term2.data["DocID"][j]:
            j += 1
        if i == len(term1.data["DocID"]) or j == len(term2.data["DocID"]):
            break
    tmp_term = Node(term)
    for string in temp_list:
        tmp_term.data["DocID"].append(string)
    return tmp_term


def get_nodes(root: Node):
    List: list[Node] = []
    Stack = []
    Stack.append(root)
    tmp = root.right
    while len(Stack) != 0 or tmp != None:
        while tmp != None:
            Stack.append(tmp)
            tmp = tmp.right
        tmp = Stack.pop()
        List.append(tmp)
        tmp = tmp.left
    return List


def get_sorted_by_docfreq(root: Node):
    all_nodes_freq = []
    Stack = []
    Stack.append(root)
    tmp = root.right
    while len(Stack) != 0 or tmp != None:
        while tmp != None:
            Stack.append(tmp)
            tmp = tmp.right
        tmp = Stack.pop()
        all_nodes_freq.append(
            {
                "term": tmp.data["term"],
                "freq": len(tmp.data["DocID"])
            }
        )
        tmp = tmp.left

    all_nodes_freq = sorted(all_nodes_freq, key=lambda d: d["freq"])
    all_nodes_freq.reverse()
    return all_nodes_freq


def Sort_freq(List):
    for n1 in List:
        for n2 in list[n1+1:]:
            if len(n1.data["DocID"]) > len(n2.data["DocID"]):
                list.index()

# ======================================
# Calculating Sizes
# ======================================


def sizeof_Index(root: Node):
    size = 0
    Stack = []
    Stack.append(root)
    tmp = root.right
    while len(Stack) != 0 or tmp != None:
        while tmp != None:
            Stack.append(tmp)
            tmp = tmp.right
        tmp = Stack.pop()
        size += asizeof.asizeof(tmp.data["term"])
        size += asizeof.asizeof(tmp.data["DocID"])
        tmp = tmp.left
    return size


def sizeof_Vocab(root: Node):
    size = 0
    Stack = []
    Stack.append(root)
    tmp = root.right
    while len(Stack) != 0 or tmp != None:
        while tmp != None:
            Stack.append(tmp)
            tmp = tmp.right
        tmp = Stack.pop()
        size += asizeof.asizeof(tmp.data["term"])
        tmp = tmp.left
    return size


def sizeof_Posting(root: Node):
    size = 0
    Stack = []
    Stack.append(root)
    tmp = root.right
    while len(Stack) != 0 or tmp != None:
        while tmp != None:
            Stack.append(tmp)
            tmp = tmp.right
        tmp = Stack.pop()
        size += asizeof.asizeof(tmp.data["DocID"])
        tmp = tmp.left
    return size
# ======================================
# Writing and Reading data with pickle
# ======================================


def WriteData(root: Node, file_name: str):
    with open(file_name + ".pkl", "wb") as file:
        pickle.dump(root, file)


def ReadData(file_name: str):
    with open(file_name + ".pkl", "rb") as file:
        root = pickle.load(file)
    return root
# ======================================
# preprocesses
# ======================================


def LowerCase(s: str):
    return s.lower()


def stopword_removal_20(root: Node, term: str, DocID: str):
    stop_words = [
        'the', 'and', 'to', 'of', 'a', 'i', 'in', 'is', 'it', 'that',
        'for', 'you', 'was', 'with', 'on', 'as', 'are', 'by', 'be', 'this'
    ]
    if LowerCase(term) not in stop_words:
        return Insert(root, term, DocID)
    else:
        return root


def stopword_removal_50(root: Node, term: str, DocID: str):
    stop_words = [
        'the', 'and', 'to', 'of', 'a', 'i', 'in', 'is', 'it', 'that',
        'for', 'you', 'was', 'with', 'on', 'as', 'are', 'by', 'be', 'this',
        'have', 'from', 'at', 'or', 'had', 'not', 'we', 'an', 'but', 'they',
        'he', 'she', 'which', 'can', 'will', 'were', 'do', 'their', 'has',
        'there', 'been', 'if', 'more', 'her', 'so', 'about', 'up', 'out',
        'then', 'them'
    ]
    if LowerCase(term) not in stop_words:
        return Insert(root, term, DocID)
    else:
        return root


def Stemming(term: str):
    return PorterStemmer().stem(term.lower())


def Lemmatizing(term: str):
    return WordNetLemmatizer().lemmatize(term.lower())


def Lossy_pruning(root: Node):
    list = []
    Stack = []
    Stack.append(root)
    tmp = root.right
    while len(Stack) != 0 or tmp != None:
        while tmp != None:
            Stack.append(tmp)
            tmp = tmp.right
        tmp = Stack.pop()
        if len(tmp.data["DocID"]) < 2:
            root = Removekey(root, tmp.data["term"])
        tmp = tmp.left
    return root


def Keep_20k_terms(root: Node, all_nodes_freq: list):
    top_terms = [item["term"] for item in all_nodes_freq[:20000]]
    nodes = []

    def inorder_collect(node):
        if node is None:
            return
        inorder_collect(node.left)
        if node.data["term"] in top_terms:
            nodes.append(node)
        inorder_collect(node.right)

    inorder_collect(root)

    if not nodes:
        return None

    def build_balanced(start, end):
        if start > end:
            return None
        mid = (start + end) // 2
        node = nodes[mid]
        node.left = None
        node.right = None
        node.left = build_balanced(start, mid - 1)
        node.right = build_balanced(mid + 1, end)
        return node

    new_root = build_balanced(0, len(nodes) - 1)

    return new_root

# Tokenization


def Tokenization():
    root = Node(data[0][1][0], data[1][0])
    n = 0
    while n < 10788:
        for term in data[n][1]:
            root = Insert(root, term, data[n][0])
            # root = Insert(root, LowerCase(term), data[n][0])
            # root = stopword_removal_20(root, term, data[n][0])
            # root = stopword_removal_50(root, term, data[n][0])
            # root = Insert(root, Stemming(term), data[n][0])
            # root = Insert(root, Lemmatizing(term), data[n][0])
        n += 1
    return root


os.system('cls')
root = Tokenization()
# root = Lossy_pruning(root) #preproce
# root = Keep_20k_terms(root, all_nodes_freq) #preproce
root_NP = ReadData("No_PreProcess")  # For Reading saved data
root_LWC = ReadData("LowerCase")
root_STPW_20 = ReadData("stopword_removal_20")
root_STPW_50 = ReadData("stopword_removal_50")
root_Stem = ReadData("Stemming")
root_Lemma = ReadData("Lemmatizing")
root_LOSPRU = ReadData("Lossy_pruning")
root_KP_20k = ReadData("Keep_20k_terms")
all_nodes_freq = get_sorted_by_docfreq(root_NP)
# WriteData(root_KP_20k, "Keep_20k_terms")  # For saving data
print(f"Size Of Index: {sizeof_Index(root_NP) / (1024**2):.2f}MB")
print(f"Size Of Vocabs: {sizeof_Vocab(root_NP) / (1024**2):.2f}MB")
print(f"Size Of Posting: {sizeof_Posting(root_NP) / (1024**2):.2f}MB")

# Menu
print("1. Search for one query")
print("2. Search for two queries with AND")
print("3. See 30 most frequent terms")
Choice = int(input("Choose an option: "))
if Choice == 1:
    query = input("Enter your query: ")
    print("No Preprocess:")
    Search(root_NP, query)
    print("\n\nWith Lower Case:")
    Search(root_LWC, LowerCase(query))
    print("\n\nWith Stop Word Removal 20:")
    Search(root_STPW_20, LowerCase(query))
    print("\n\nWith Stop Word Removal 50:")
    Search(root_STPW_50, LowerCase(query))
    print("\n\nWith Stemming:")
    Search(root_Stem, Stemming(query))
    print("\n\nWith Lemmatizing:")
    Search(root_Lemma, Lemmatizing(query))
    print("\n\nWith Lossy Pruning:")
    Search(root_LOSPRU, query)
    print("\n\nWith Keeping 20k Terms:")
    Search(root_KP_20k, query)


elif Choice == 2:
    query = input("Enter your query: ").lower()
    print("No Preprocess:")
    Search_with_AND(root_NP, query)
    print("\n\nWith Lower Case:")
    Search_with_AND(root_LWC, LowerCase(query))
    print("\n\nWith Stop Word Removal 20:")
    Search_with_AND(root_STPW_20, LowerCase(query))
    print("\n\nWith Stop Word Removal 50:")
    Search_with_AND(root_STPW_50, LowerCase(query))
    print("\n\nWith Stemming:")
    Search_with_AND(root_Stem, Stemming(query))
    print("\n\nWith Lemmatizing:")
    Search_with_AND(root_Lemma, Lemmatizing(query))
    print("\n\nWith Lossy Pruning:")
    Search_with_AND(root_LOSPRU, query)
    print("\n\nWith Keeping 20k Terms:")
    Search_with_AND(root_KP_20k, query)
elif Choice == 3:
    n = 1
    for x in all_nodes_freq:
        print(f"{n}-{x["term"]}, {x["freq"]}")
        n += 1
        if n == 31:
            break

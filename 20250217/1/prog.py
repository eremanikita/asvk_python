import zlib
from sys import argv
from glob import iglob
from os.path import basename
from pathlib import Path


def find_branches(repo_link):
    return iglob(repo_link + "/refs/heads/*")


def get_last_commit_hash(branches_list, branch_name):
    for branch in branches_list:
        if basename(branch) == branch_name:
            required_branch = branch
            break
    else:
        print(f"Не найдено ветки {branch_name}.")
        exit()

    with open(required_branch, "r") as f:
        return f.read().rstrip()


def get_tree_name(blob):
    for line in blob.splitlines():
        if line.startswith("tree"):
            return line.split()[1]


def parse_tree_object(tree_data):
    _, _, content = tree_data.partition(b'\x00')
    files = []
    while content:
        mode_name, content = content.split(b'\x00', 1)
        mode, name = mode_name.split(b' ', 1)
        sha1, content = content[:20], content[20:]
        sha1_hex = sha1.hex()
        files.append(" ".join([mode.decode(), name.decode(), sha1_hex]))

    return files


def show_commit_history(commit_hash):
    tmp_commit = zlib.decompress(Path(argv[1] + f"/objects/{commit_hash[:2]}/{commit_hash[2:]}").read_bytes())
    head, _, blob = tmp_commit.partition(b'\x00')
    blob = blob.decode()
    tree_name = get_tree_name(blob)
    tree_object = zlib.decompress(Path(argv[1] + f"/objects/{tree_name[:2]}/{tree_name[2:]}").read_bytes())
    print(f"TREE for commit {commit_hash}")
    print(*parse_tree_object(tree_object))
    for line in blob.splitlines():
        if line.startswith("parent"):
            show_commit_history(line.split()[1])


match len(argv):
    case 1:
        print("Ошибка ввода параметров. Должен быть передан путь к репозиторию.")
    case 2:
        for branch in find_branches(argv[1]):
            print(basename(branch))
    case 3:
        last_commit = get_last_commit_hash(find_branches(argv[1]), argv[2])

        commit_object = zlib.decompress(
            Path(argv[1] + f"/objects/{last_commit[:2]}/{last_commit[2:]}").read_bytes())
        head, _, blob = commit_object.partition(b'\x00')
        blob = blob.decode()
        print(blob)

        show_commit_history(last_commit)

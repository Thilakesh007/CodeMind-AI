import os


SUPPORTED_EXTENSIONS = [
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".cpp",
    ".c",
    ".html",
    ".css",
    ".txt",
    ".md"
    
]


def read_repository(repo_path):

    files = []

    for root, dirs, filenames in os.walk(repo_path):

        for filename in filenames:

            ext = os.path.splitext(filename)[1]

            if ext in SUPPORTED_EXTENSIONS:

                path = os.path.join(
                    root,
                    filename
                )

                try:
                    with open(
                        path,
                        "r",
                        encoding="utf-8",
                        errors="ignore"
                    ) as file:

                        content = file.read()

                        files.append(
                            {
                                "file": path,
                                "content": content
                            }
                        )

                except Exception as e:
                    print(
                        "Error reading",
                        path,
                        e
                    )

    return files
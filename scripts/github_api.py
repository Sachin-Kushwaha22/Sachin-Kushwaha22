import requests
from config import GITHUB_USERNAME, GITHUB_TOKEN, GRAPHQL_URL


class GitHubAPI:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Content-Type": "application/json",
        }

    def run_query(self, query, variables=None):
        response = requests.post(
            GRAPHQL_URL,
            json={"query": query, "variables": variables or {}},
            headers=self.headers,
        )

        if response.status_code != 200:
            raise Exception(f"GitHub API Error {response.status_code}\n{response.text}")

        data = response.json()

        if "errors" in data:
            raise Exception(data["errors"])

        return data["data"]

    def get_profile(self):
        query = """
        query($username: String!) {
        user(login: $username) {

            name
            login
            bio
            avatarUrl

            followers {
            totalCount
            }

            following {
            totalCount
            }

            repositories(
            ownerAffiliations: OWNER
            isFork: false
            first: 100
            ) {

            totalCount

            nodes {

                name

                stargazerCount

                forkCount

                issues(states: OPEN) {
                totalCount
                }

                pullRequests {
                totalCount
                }

                languages(first:10, orderBy:{field:SIZE,direction:DESC}) {

                edges{

                    size

                    node{

                    name

                    }

                }

                }

            }

            }

        }

        }
        """

        data = self.run_query(
            query,
            {"username": GITHUB_USERNAME}
        )

        return data["user"]


if __name__ == "__main__":
    github = GitHubAPI()

    profile = github.get_profile()

    print(f"Name: {profile['name']}")
    print(f"Followers: {profile['followers']['totalCount']}")
    print(f"Following: {profile['following']['totalCount']}")
    print(f"Repositories: {profile['repositories']['totalCount']}")

    stars = 0

    for repo in profile["repositories"]["nodes"]:
        stars += repo["stargazerCount"]

    print(f"Total Stars: {stars}")

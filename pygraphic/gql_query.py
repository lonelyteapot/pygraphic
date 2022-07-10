from .gql_type import GQLType


class GQLQuery(GQLType):
    @classmethod
    def get_query_string(cls) -> str:
        def _gen():
            yield "query {"
            for line in cls.generate_query_lines():
                yield line
            yield "}"

        return "\n".join(_gen())

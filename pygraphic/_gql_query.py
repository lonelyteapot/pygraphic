from ._gql_type import GQLType


class GQLQuery(GQLType):
    @classmethod
    def get_query_string(cls, named: bool = True) -> str:
        def _gen():
            if named:
                yield "query " + cls.__name__ + " {"
            else:
                yield "query {"
            for line in cls.generate_query_lines(nest_level=1):
                yield line
            yield "}"

        return "\n".join(_gen())

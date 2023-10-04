import pymongo


class EasyMongoDB:
    """The MongoDB class helps simplify the use of MongoDB for Python"""

    def __init__(
        self,
        username: str,
        password: str,
        database: str,
        **kwargs
    ):
        """
        Constructs all the necessary attributes for the MongoDB object.

        Parameters
        ----------
            username : str
                the username of the account that connects to the MongoDB server
            password : str
                the password of the provided username
            database : str
                the name of the database you want to connect to
        """

        host = kwargs.get("host", "mongodb://localhost:27017/")
        authentication_source = kwargs.get("authentication_source", "admin")
        authentication_mechanism = kwargs.get(
            "authentication_mechanism", "SCRAM-SHA-256")

        mongo_client = pymongo.MongoClient(
            host,
            username=username,
            password=password,
            authSource=authentication_source,
            authMechanism=authentication_mechanism
        )

        self.mongo_db = mongo_client[database]

    def add_single_document(
        self,
        collection: str,
        data_package: dict
    ):
        """
        Adds a single document to a MongoDB collection.

        Parameters
        ----------
            collection : str
                the name of the collection
            data_package : dict
                the dictionary containing the data of the document you want to
                add
        """

        return self.mongo_db[collection].insert_one(data_package)

    def add_multiple_documents(
        self,
        collection: str,
        data_packages: list
    ):
        """
        Adds a multiple documents to a MongoDB collection.

        Parameters
        ----------
            collection : str
                the name of the collection
            data_packages : list
                the list containing the dictionaries to add to the collection
        """

        self.mongo_db[collection].insert_many(data_packages)

    def drop_collection(
        self,
        collection: str
    ):
        """
        Drops a MongoDB collection.

        Parameters
        ----------
            collection : str
                the name of the collection
        """

        self.mongo_db[collection].drop()

    def get_documents(
        self,
        collection: str,
        **kwargs
    ):
        """
        Retrieve documents from a MongoDB collection.

        Parameters
        ----------
            collection : str
                the name of the collection
        """
        if "query_filter" in kwargs and "sort" in kwargs:
            return self.mongo_db[collection].find(
                kwargs.get("query", {}),
                kwargs["query_filter"],
                sort=kwargs["sort"]
            ).batch_size(kwargs.get("batch_size", 0))

        if "query_filter" in kwargs:
            return self.mongo_db[collection].find(
                kwargs.get("query", {}),
                kwargs["query_filter"]
            ).batch_size(kwargs.get("batch_size", 0))

        if "sort" in kwargs:
            return self.mongo_db[collection].find(
                kwargs.get("query", {}),
                sort=kwargs["sort"]
            ).batch_size(kwargs.get("batch_size", 0))

        return self.mongo_db[collection].find(kwargs.get("query", {})).batch_size(kwargs.get("batch_size", 0))

    def update_documents(
        self,
        collection: str,
        query: dict,
        data: dict
    ):
        """
        Update documents in a MongoDB collection.

        Parameters
        ----------
            collection : str
                the name of the collection
            query : dict
                dictionary containing the parameters which the query needs
                to meet
            data : dict
                dictionary containing data that needs to be updated
        """

        return self.mongo_db[collection].update_many(query, {"$set": data})

    def aggregate_collection(
        self,
        collection: str,
        query: dict,
        allow_disk: bool = True
    ):
        """
        Returns an aggrated result from a MongoDB collection.

        Parameters
        ----------
            collection : str
                the name of the collection
            query : dict
                dictionary containing the parameters which the query needs
                to meet
            allow_disk : bool
                boolean which determins whether to write temporary files to the
                hard disk
        """

        return self.mongo_db[collection].aggregate(query, allowDiskUse=allow_disk)

    def delete_single_document(
        self,
        collection: str,
        query: dict
    ):
        """
        Delete a single document from a MongoDB collection.

        Parameters
        ----------
            collection : str
                the name of the collection
            query : dict
                dictionary containing the parameters which the query needs
                to meet
        """

        self.mongo_db[collection].delete_one(query)

    def delete_multiple_documents(
        self,
        collection: str,
        query: dict
    ):
        """
        Delete multiple documents from a MongoDB collection.

        Parameters
        ----------
            collection : str
                the name of the collection
            query : dict
                dictionary containing the parameters which the query needs
                to meet
        """

        self.mongo_db[collection].delete_many(query)

    def create_index(
        self,
        collection: str,
        fields: list
    ):
        """
        Creates one or more indexes in a MongoDB collection.

        Parameters
        ----------
            collection : str
                the name of the collection
            fields : list
                list containing dictionarues with field names and direction
                which will be the indexes of the collection. Direction can
                be descending or ascending. A dictionary looks like
                {field: fieldname, direction: ascending}
        """

        parsed_fields = []

        for item in fields:
            if item["direction"] == "descending":
                parsed_fields.append((item["field"], pymongo.DESCENDING))
            elif item["direction"] == "ascending":
                parsed_fields.append((item["field"], pymongo.ASCENDING))

        self.mongo_db[collection].create_index(parsed_fields, unique=True)

    def collection_exists(
        self,
        collection: str
    ):
        """
        Checks whether a MongoDB collection exists.

        Parameters
        ----------
            collection : str
                the name of the collection
        """

        if collection in self.mongo_db.list_collection_names():
            return True

        return False

    def get_distinct_documents(
        self,
        collection: str,
        field: str,
        **kwargs
    ):
        """
        Returns documents with distinct values in a given field from a MongoDB
        collection.

        Parameters
        ----------
            collection : str
                the name of the collection
            field : str
                string with the field name that needs to have a distinct value
            query : dict
                dictionary containing the parameters which the query needs
                to meet
        """

        if "query" not in kwargs:
            return self.mongo_db[collection].distinct(field)

        return self.mongo_db[collection].distinct(field, kwargs.get("query", {}))

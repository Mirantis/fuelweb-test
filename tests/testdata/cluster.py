class TD_Cluster(object):
    NAME = "cluster"

    def __init__(self):
        super(TD_Cluster, self).__init__()
        self.name = ""
        self.version = ""

    def __repr__(self):
        return str(dict(
            class_name="TD_Cluster",
            name=self.name,
            version=self.version
        ))

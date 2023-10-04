from synapsis import Synapsis


class EntityBundleWrapper:
    def __init__(self, bundle=None):
        self.bundle = bundle or {}
        self._concrete_type = Synapsis.ConcreteTypes.get(self.bundle)

    @classmethod
    async def fetch(cls, synapse_id, **kwargs):
        bundle = await Synapsis.Chain.Utils.get_bundle(synapse_id, **kwargs)
        return cls(bundle=bundle)

    @property
    def entity_type(self):
        return self.bundle.get('entityType')

    @property
    def concrete_type(self):
        return self._concrete_type

    @property
    def is_project(self):
        return self.concrete_type.is_project

    @property
    def is_folder(self):
        return self.concrete_type.is_folder

    @property
    def is_file(self):
        return self.concrete_type.is_file

    def is_a(self, *concrete_types):
        return self.concrete_type.is_a(*concrete_types)

    @property
    def entity(self):
        return self.bundle.get('entity')

    @property
    def id(self):
        return self.entity.get('id')

    @property
    def name(self):
        return self.entity.get('name')

    @property
    def has_children(self):
        return self.bundle.get('hasChildren', False)

    @property
    def data_file_handle_id(self):
        return self.entity.get('dataFileHandleId')

    @property
    def synapse_path(self):
        path = None
        if self.bundle and 'path' in self.bundle:
            paths = self.bundle.get('path').get('path')[1:]
            segments = []
            for path in paths:
                segments.append(path['name'])
            path = '/'.join(segments)

        return path

    @property
    def file_handle(self):
        file_handle = None
        if self.bundle.get('fileHandles'):
            file_handle = Synapsis.Utils.find_data_file_handle(self.bundle,
                                                               data_file_handle_id=self.data_file_handle_id)
        return file_handle

    @property
    def filename(self):
        file_handle = self.file_handle
        return file_handle['fileName'] if file_handle else None

    @property
    def content_md5(self):
        file_handle = self.file_handle
        return file_handle['contentMd5'] if file_handle else None

    @property
    def content_size(self):
        file_handle = self.file_handle
        return file_handle['contentSize'] if file_handle else None

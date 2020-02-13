#engine version class
class ClientEngineVersion():
    def __init__(self, version, name):
        try:
            self.version = version
            self.name = name
            self.title = self.name+' (v.'+str(version)+')'

            pass
        except Exception as e:
            pass

#client settings
class ClientSettingsModel():
    def __init__(self):
        try:
            self.client_id = -1
            self.engine_number = -1
            self.show_project_error_states = True
            self.show_project_registration_number_column = True
            self.show_products_form = False
            self.show_project_log = True
            self.show_project_discussion = True
            self.show_project_files = True
            self.show_project_history = True
            self.export_original_documents =True
            self.show_consolidation_static_files = True


            self.engine_versions = []
            self.init_engine_versions()
        except Exception as e:
            pass

    #init single version
    def init_version(self,version, name):
        try:
            self.engine_versions.append(ClientEngineVersion(version,name))
        except Exception as e:
            pass

    #init all engine versions
    def init_engine_versions(self):
        try:
            self.init_version('1','Puzzle')
            self.init_version('2','Mosaic')
            self.init_version('3','Kaleidoscope')
            self.init_version('4','Beads')

            pass
        except Exception as e:
            pass
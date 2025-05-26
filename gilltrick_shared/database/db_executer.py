import datetime, re

class Executer:
    def __init__(self, connection, config):
        self.connection = connection
        self.config = config

    def create_video(self, id, original_filename, filename, title, description, duration, categories, sub_categories, tags, visibility, happy_ends, timestamps, url, thumbnail_url, owner_id, free, public, trailer):
        rc, result = self.connection.execute(f'''insert into {self.config["database"]["name"]}.{self.config["database"]["tables"][0]["name"]} (
                                id,
                                original_filename,
                                filename, 
                                title,             
                                description, 
                                duration, 
                                categories, 
                                sub_categories, 
                                tags,
                                visibility,
                                happy_ends,
                                timestamps,
                                url,
                                thumbnail_url,
                                owner_id,                                  
                                created_at,
                                updated_at,
                                free,
                                public,
                                trailer) 
                                values (
                                '{id}',
                                '{original_filename}',
                                '{filename}', 
                                '{title}', 
                                '{description}', 
                                '{duration}', 
                                '{categories}',
                                '{sub_categories}',
                                '{tags}',
                                '{visibility}',
                                '{happy_ends}',
                                '{timestamps}',
                                '{url}',
                                '{thumbnail_url}',
                                '{owner_id}',
                                '{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}',
                                '{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}',
                                {free},
                                {public},
                                {trailer})''')
        return result
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from base import Base
from json import loads


# ! TEST NON FONCTIONNEL : erreur => "sqlalchemy.orm.exc.UnmappedInstanceError: Class 'builtins.list' is not mapped" !

class TestApi(Base):
    def test_amendes(self):
        """ Vérifie qu'une amende est bien traitée """
        self.insert_all()
        response = self.client.get("/api/amende/1")
        # Le corps de la réponse est dans .data
        # .data est en "bytes". Pour convertir des bytes en str, on fait .decode()
        content = response.data.decode()
        self.assertEqual(
            response.headers["Content-Type"], "application/json"
        )
        json_parse = loads(content)
        self.assertEqual(json_parse["type"], "amende")
        self.assertEqual(
            json_parse["attributes"]["amendes_franche_verite"], "non")
        self.assertEqual(json_parse["attributes"]["amendes_id"], 1)
        self.assertEqual(json_parse["attributes"]["amendes_montant"], 60)
        self.assertEqual(json_parse["attributes"]["amendes_personnes_id"], 1)
        self.assertEqual(json_parse["attributes"]["amendes_source_id"], 6234)
        self.assertEqual(json_parse["attributes"]["amendes_transcription"], "Pour avoir pris et emporté certaines cloyes appartenant à aultruy receu LX sous")
        self.assertEqual(json_parse["attributes"]["amendes_type"], "vol")
        self.assertEqual(json_parse["id"], '1')
        self.assertEqual(json_parse["links"]["json"], "http://127.0.0.1:5000/api/amende/1")
        self.assertEqual(json_parse["links"]["justiciables(personnes)"], "http://127.0.0.1:5000/api/personne/1")
        self.assertEqual(json_parse["links"]["self"], "http://127.0.0.1:5000/amende/1")
        self.assertEqual(json_parse["links"]["source"], "http://127.0.0.1:5000/api/source/6234/amende/1")
        # self.assertEqual(json_parse["relationships"],
        #                  {"editions": [
        #                      {
        #                          "author": {
        #                              "attributes": {
        #                                  "name": "decraene"
        #                              },
        #                              "type": "people"
        #                          },
        #                          "on": "Thu, 17 Feb 2022 14:57:16 GMT"
        #                      },
        #                      {
        #                          "author": {
        #                              "attributes": {
        #                                  "name": "decraene"
        #                              },
        #                              "type": "people"
        #                          },
        #                          "on": "Thu, 17 Feb 2022 14:57:21 GMT"
        #                      }
        #                  ]
        #                  })
        self.assertEqual(json_parse["type"], 'amende')

        # On vérifie que le lien est correct
        seconde_requete = self.client.get(json_parse["links"]["self"])
        self.assertEqual(seconde_requete.status_code, 200)

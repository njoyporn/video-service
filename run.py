# from backend_shared.api import router
# from backend_shared.configurator import Configurator
# configurator = Configurator()
# configurator.load_config()
# router.run(configurator.config)


from backend_shared.api import router
from backend_shared.configurator import Configurator
from backend_shared.database import setup as dbSetup
from backend_shared.security import setup as securitySetup
import os

configurator = Configurator(f"{os.getcwd()}/config/video.config.json")
configurator.load_config()
security_setup = securitySetup.Setup(configurator.config)
security_setup.setup_keys()
db_setup = dbSetup.Setup(configurator.config)
db_setup.init_db()
router.run(configurator.config)
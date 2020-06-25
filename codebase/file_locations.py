# ========================================
#   Copier Queues
# ========================================

def copieractionqueue():
	return "./data/copier_queue"

def filesystemdataqueue():
	return "./data/filesystem_data"



# ========================================
#   Deluge Operator Queues
# ========================================

def operatoractionqueue():
	return "./data/operator_queue"

def sessiondataqueue():
	return "./data/session_data"

def historydataqueue():
	return "./data/history_data"



# ========================================
#   Application Configurations
# ========================================

def operatorapplicationconfiguration():
	return "./data/application_config/operator_connection.cfg"

def copierapplicationconfiguration():
	return "./data/application_config/copier_connection.cfg"



# ========================================
#   Application Restart Caches
# ========================================

def torrentconfigurations():
	return "./data/torrent_configs"

def copierhistory():
	return "./data/copier_actions"




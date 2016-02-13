import sys
import datetime
import MySQLdb
con = MySQLdb.connect('localhost', 'root', 'root', 'xo_db')
#date = sys.argv[1]
#str_dates = date.split('-')
#year = int(str_dates[0])
#mm = int(str_dates[1])
#dd = int(str_dates[2])
sql_create_table = "CREATE TABLE IF NOT EXISTS stat_player_games(" \
                   "id INT AUTO_INCREMENT," \
                   "target_date DATE," \
                   "game_count INT," \
                   "xp_amount INT," \
                   "created DATETIME," \
                   "PRIMARY KEY (id) );"
cur = con.cursor()
cur.execute(sql_create_table)

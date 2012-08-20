# TODO: Make this rely on things that are not straight-up exec.
class balrog {
    # create config files
    file {
        "/etc/aus/admin.ini":
            content => template("vagrant/admin.ini.erb")
        "/etc/aus/balrog.ini":
            content => template("vagrant/balrog.ini.erb")
    }
    # import mysqldump
    exec { "create_mysql_database":
        command => "mysql -uroot -B -e'CREATE DATABASE $DB_NAME CHARACTER SET utf8;'",
        unless  => "mysql -uroot -B --skip-column-names -e 'show databases' | /bin/grep '$DB_NAME'",
    }

    exec { "grant_mysql_database":
        command => "mysql -uroot -B -e'GRANT ALL PRIVILEGES ON $DB_NAME.* TO $DB_USER@localhost # IDENTIFIED BY \"$DB_PASS\"'",
        unless  => "mysql -uroot -B --skip-column-names mysql -e 'select user from user' | grep '$DB_USER'",
        require => Exec["create_mysql_database"];
    }
    exec { "grant_ro_mysql_database":
        command => "mysql -uroot -B -e'GRANT SELECT ON $DB_NAME.* TO $DB_RO_USER@localhost # IDENTIFIED BY \"$DB_RO_PASS\"'",
        unless  => "mysql -uroot -B --skip-column-names mysql -e 'select user from user' | grep '$DB_RO_USER'",
        require => Exec["create_mysql_database"];
    }
}

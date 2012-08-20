MOUNT_POINT = '/home/vagrant/project'

Vagrant::Config.run do |config|
    config.vm.box = "centos-netboot"
    config.vm.box_url = "http://dl.dropbox.com/u/9227672/CentOS-6.0-x86_64-netboot-4.1.6.box"

    config.vm.forward_port 8000, 8000

    # Increase vagrant's patience during hang-y CentOS bootup
    # see: https://github.com/jedi4ever/veewee/issues/14
    config.ssh.max_tries = 50
    config.ssh.timeout   = 300

    config.vm.share_folder("v-root", MOUNT_POINT, ".")

    # Add to /etc/hosts:
    #  33.33.33.24 aus4-admin-dev.allizom.org
    #  33.33.33.24 aus4-dev.allizom.org
    config.vm.network :hostonly, "33.33.33.24"

    config.vm.provision :puppet do |puppet|
        puppet.manifests_path = "puppet/manifests"
        puppet.manifest_file  = "vagrant.pp"
    end
end

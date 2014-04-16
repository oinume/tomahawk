# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  #
  # CentOS 5.10
  #
  config.vm.define "centos_5_10" do |centos_5_10|
    centos_5_10.vm.name = "tomahawk-centos-5.10"
    centos_5_10.vm.box = "chef/centos-5.10"
    centos_5_10.vm.network "private_network", ip: "192.168.33.234"
    # Create a public network, which generally matched to bridged network.
    # Bridged networks make the machine appear as another physical device on
    # your network.
    # config.vm.network "public_network"

    # If true, then any SSH connections made will enable agent forwarding.
    # Default value: false
    # config.ssh.forward_agent = true

    # Share an additional folder to the guest VM. The first argument is
    # the path on the host to the actual folder. The second argument is
    # the path on the guest to mount the folder. And the optional third
    # argument is a set of non-required options.
    # centos_5_10.vm.synced_folder ".", "/tomahawk"

    centos_5_10.vm.provider "virtualbox" do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512"]
    end

    #centos_5_10.vm.provision "shell", inline: "sudo yum groupinstall -y 'Development Tools'"
    centos_5_10.vm.provision "shell", inline: "sudo yum install -y gcc python-setuptools python-devel"
    centos_5_10.vm.provision "shell", inline: "sudo easy_install https://github.com/pypa/pip/archive/1.1.tar.gz"
    centos_5_10.vm.provision "shell", inline: "cd /vagrant && sudo pip install -e ."
  end

end

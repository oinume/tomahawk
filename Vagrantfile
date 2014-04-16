# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  #
  # CentOS 5.10
  # vagrant up centos_5_10
  #
  config.vm.define "centos_5_10" do |centos_5_10|
    #centos_5_10.vm.name = "tomahawk-centos-5.10"
    centos_5_10.vm.box = "chef/centos-5.10"
    centos_5_10.vm.network "private_network", ip: "192.168.33.234"
    # config.vm.network "public_network"

    # If true, then any SSH connections made will enable agent forwarding.
    # Default value: false
    # config.ssh.forward_agent = true
    # centos_5_10.vm.synced_folder ".", "/tomahawk"

    centos_5_10.vm.provider "virtualbox" do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512"]
    end

    centos_5_10.vm.provision "shell", inline: "sudo yum install -y gcc python-setuptools python-devel"
    centos_5_10.vm.provision "shell", inline: "sudo easy_install https://github.com/pypa/pip/archive/1.1.tar.gz"
    centos_5_10.vm.provision "shell", inline: "cd /vagrant && sudo pip install -e ."
  end

  #
  # CentOS 6.5
  # vagrant up centos_6_5
  #
  config.vm.define "centos_6_5" do |centos_6_5|
    #centos_6_5.vm.name = "tomahawk-centos-6.5"
    centos_6_5.vm.box = "chef/centos-6.5"
    centos_6_5.vm.network "private_network", ip: "192.168.33.235"
    # config.vm.network "public_network"

    # If true, then any SSH connections made will enable agent forwarding.
    # Default value: false
    # config.ssh.forward_agent = true
    # centos_6_5.vm.synced_folder ".", "/tomahawk"

    centos_6_5.vm.provider "virtualbox" do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512"]
    end

    centos_6_5.vm.provision "shell", inline: "sudo yum install -y gcc python-setuptools python-devel"
    centos_6_5.vm.provision "shell", inline: "sudo easy_install pip"
    centos_6_5.vm.provision "shell", inline: "cd /vagrant && sudo pip install -e ."
  end
end

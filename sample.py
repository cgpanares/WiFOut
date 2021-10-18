from fabric import env

def hostname():

    env.hosts = ['myhosts']

def mycmd():
    print env.hosts
    run('ls -l')

mycmd()

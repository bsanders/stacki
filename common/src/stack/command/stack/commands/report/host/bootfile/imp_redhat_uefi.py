#
# @SI_COPYRIGHT@
# @SI_COPYRIGHT@
#

import stack.commands

install_template = """set gfxpayload=keep
insmod gzio
insmod part_gpt
insmod ext2

set timeout=5

menuentry "Stacki UEFI Install" {
	echo "Loading %s"
	linuxefi /%s %s
	echo "Loading %s"
	initrdefi /%s
}
"""

os_template = """search.fs_uuid %s root
configfile ($root)/efi/centos/grub.cfg
"""


class Implementation(stack.commands.Implementation):
	def run(self, h):
		host     = h['host']
		kernel   = h['kernel']
		ramdisk  = h['ramdisk']
		args     = h['args']
		boottype = h['type']


		# Get the bootaction for the host (install or os) and
		# lookup the actual kernel, ramdisk, and args for the
		# specific action.
		root_uuid = None
		if boottype == 'os':
			for part in self.owner.call('list.host.partition', [host]):
				if part['mountpoint'] == '/boot/efi':
					root_uuid = part['uuid']
					break
			if root_uuid:
				self.owner.addOutput(host, os_template % root_uuid)

		else:
			args = "%s BOOTIF=$net_default_mac" % args
			self.owner.addOutput(host, install_template % (kernel, kernel, args, ramdisk, ramdisk))

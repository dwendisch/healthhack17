module.exports = function(grunt) {

	var Settings = {
		raspberry_ip: grunt.option("ip") || "192.168.0.9",
		watch: {
			all: {
				files: ["app/**/*", "configs/**/*"],
				tasks: ["scp:code", "scp:configs"],
				options: {
					spawn: false,
				},
			},
			code: {
				files: ["app/**/*"],
				tasks: ["scp:code"],
				options: {
					spawn: false,
				},
			},
			configs: {
				files: ["configs/**/*"],
				tasks: ["scp:configs"],
				options: {
					spawn: false,
				},
			},
		},
		scp: {
			options: {
				host: "<%= raspberry_ip %>",
				username: "pi",
				password: "raspberry"
			},
			configs: {
				files: [{
					cwd: "configs/",
					src: "**",
					filter: "isFile",
					dest: "/home/pi/configs/"
				}]
			},
			code: {
				files: [{
					cwd: "app/",
					src: "**/*",
					filter: "isFile",
					dest: "/home/pi/app/"
				}]
			}
		},

		copy: {
			wifi: {
				files: [{
					expand: true,
					cwd: "configs/wifi/",
					src: "*",
					dest: "/Volumes/boot/"
				}]
			}
		},

		shell: {
			install: {
				command: "sudo dd bs=1m if=2017-03-02-raspbian-jessie-lite.img of=/dev/rdisk3 && echo 'Done'",
				options: {
					callback: function (err, stdout, stderr, cb) {
						console.log("Installing done, moving on in 5s...");
						setTimeout(cb, 5000);
					}
				}
			},
			format_sd: {
				command: "sudo diskutil eraseDisk FAT32 RASPBIAN MBRFormat /dev/disk3"
			},
			mount: {
				command: "diskutil mountDisk /dev/disk3"
			},
			unmount: {
				command: "diskutil unmountDisk /dev/disk3"
			},
			find_ip: {
				command: 'arp -a | grep "raspberry"',
				options: {
					callback: function (err, stdout, stderr, cb) {
						if(err) grunt.log.error("Couldn't find raspberry pi ip.")
						else Settings.raspberry_ip = /\(([^)]+)\)/.exec(stdout)[1];
						cb();
					}
				}
			}
		},

		notify: {
			install_done: {
				options: {
					title: "Installation done",
					message: "SD card is unmounted"
				}
			},
		}
	};

	grunt.initConfig(Settings);

	grunt.loadNpmTasks("grunt-scp");
	grunt.loadNpmTasks("grunt-contrib-watch");
	grunt.loadNpmTasks("grunt-contrib-copy");
	grunt.loadNpmTasks("grunt-shell");
	grunt.loadNpmTasks('grunt-notify');

	grunt.registerTask("default", 	["shell:find_ip", "scp:code", "scp:configs", "watch:all"]);
	grunt.registerTask("watcher", 	["scp:code", "scp:configs", "watch:all"]);
	grunt.registerTask("pre", 		["shell:mount", "shell:format_sd", "shell:unmount", "shell:install", "copy:wifi", "shell:unmount"]);
	grunt.registerTask("post", 		["shell:mount", "copy:wifi", "shell:unmount"]);
	grunt.registerTask("unmount", 	["shell:unmount"]);
	grunt.registerTask("adhoc", 	["scp:adhoc"]);
	grunt.registerTask("ip", 		["shell:find_ip"]);
};
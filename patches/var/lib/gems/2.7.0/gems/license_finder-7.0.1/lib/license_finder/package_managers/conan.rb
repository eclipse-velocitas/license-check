# frozen_string_literal: true

require 'license_finder/package_utils/conan_info_parser'

module LicenseFinder
  class Conan < PackageManager
    def possible_package_paths
      [project_path.join('conanfile.py'), project_path.join('conanfile.txt')]
    end

    def current_packages
      install_command = 'conan install .'
      info_command = 'conan info .'
      _stdout, _stderr, _status = Dir.chdir(project_path) { Cmd.run(install_command) }
      if not _status.success?
        logger.info self.class, "Error while running 'conan install':"
        logger.debug self.class, "#{_stdout}"
        logger.debug self.class, "#{_stderr}"
        logger.info self.class, "Most/all packages will be rated having an unknown license!"
      end
      info_output, _stderr, _status = Dir.chdir(project_path) { Cmd.run(info_command) }

      info_parser = ConanInfoParser.new

      deps = info_parser.parse(info_output)
      deps.map do |dep|
        name, version = dep['name'].split('/')
        url = dep['URL']
        license_file_path = Dir.glob("#{project_path}/licenses/#{name}/**/LICENSE*").first
        ConanPackage.new(name, version, license_file_path ? File.open(license_file_path).read : "", url) unless name.start_with?("conanfile.py", "conanfile.txt")
      end.compact
    end
  end
end

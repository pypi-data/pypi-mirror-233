import os
import re


class LinguistGenerated:
    PROTOBUF_EXTENSIONS = ['.py', '.java', '.h', '.cc', '.cpp', '.m', '.rb', '.php']
    APACHE_THRIFT_EXTENSIONS = ['.rb', '.py', '.go', '.js', '.m', '.java', '.h', '.cc', '.cpp', '.php']

    def __init__(self, name, data):
        self.name = name
        self.extname = os.path.splitext(name)[1]
        self._data = data
        self._lines = None

    @property
    def data(self):
        if self._data is None:
            if callable(self._data):
                self._data = self._data()
        return self._data

    @property
    def lines(self):
        if self._lines is None:
            self._lines = self.data.split("\n") if self.data else []
        return self._lines

    def generated(self):
        return self.xcode_file() or \
            self.intellij_file() or \
            self.cocoapods() or \
            self.carthage_build() or \
            self.generated_graphql_relay() or \
            self.generated_net_designer_file() or \
            self.generated_net_specflow_feature_file() or \
            self.composer_lock() or \
            self.cargo_lock() or \
            self.flake_lock() or \
            self.node_modules() or \
            self.go_vendor() or \
            self.go_lock() or \
            self.poetry_lock() or \
            self.pdm_lock() or \
            self.esy_lock() or \
            self.npm_shrinkwrap_or_package_lock() or \
            self.terraform_lock() or \
            self.generated_yarn_plugnplay() or \
            self.godeps() or \
            self.generated_by_zephir() or \
            self.htmlcov() or \
            self.minified_files() or \
            self.has_source_map() or \
            self.source_map() or \
            self.compiled_coffeescript() or \
            self.generated_parser() or \
            self.generated_net_docfile() or \
            self.generated_postscript() or \
            self.compiled_cython_file() or \
            self.pipenv_lock() or \
            self.generated_go() or \
            self.generated_protocol_buffer_from_go() or \
            self.generated_protocol_buffer() or \
            self.generated_javascript_protocol_buffer() or \
            self.generated_apache_thrift() or \
            self.generated_jni_header() or \
            self.vcr_cassette() or \
            self.generated_antlr() or \
            self.generated_module() or \
            self.generated_unity3d_meta() or \
            self.generated_racc() or \
            self.generated_jflex() or \
            self.generated_grammarkit() or \
            self.generated_roxygen2() or \
            self.generated_jison() or \
            self.generated_grpc_cpp() or \
            self.generated_dart() or \
            self.generated_perl_ppport_header() or \
            self.generated_gamemakerstudio() or \
            self.generated_gimp() or \
            self.generated_html()

    def xcode_file(self):
        return self.extname in ['.nib', '.xcworkspacedata', '.xcuserstate']

    def intellij_file(self):
        return bool(re.match(r'(?:^|/)\.idea/', self.name))

    def cocoapods(self):
        return bool(re.match(r'(?:^|/)Pods/', self.name))

    def carthage_build(self):
        return self.name.startswith("Carthage/Build/")

    def generated_graphql_relay(self):
        return self.name.endswith(".graphql.swift")

    def generated_net_designer_file(self):
        return self.extname == ".Designer.cs"

    def generated_net_specflow_feature_file(self):
        return self.extname == ".feature.cs"

    def composer_lock(self):
        return self.name == "composer.lock"

    def cargo_lock(self):
        return self.name == "Cargo.lock"

    def flake_lock(self):
        return self.name == "flake.lock"

    def node_modules(self):
        return self.name == "node_modules"

    def go_vendor(self):
        return self.name == "vendor"

    def go_lock(self):
        return self.name == "go.sum" or self.name == "go.mod"

    def poetry_lock(self):
        return self.name == "poetry.lock"

    def pdm_lock(self):
        return self.name == "pdm.lock"

    def esy_lock(self):
        return self.name == "esy.lock"

    def npm_shrinkwrap_or_package_lock(self):
        return self.name == "npm-shrinkwrap.json" or self.name == "package-lock.json"

    def terraform_lock(self):
        return self.name == "terraform.lock.hcl"

    def generated_yarn_plugnplay(self):
        return self.name == ".yarnrc.yml" or re.match(r'(^|/)\.pnp\..*$', self.name)

    def godeps(self):
        return self.name == "Godeps"

    def generated_by_zephir(self):
        return re.match(r'.\.zep\.(?:c|h|php)$', self.name)

    def htmlcov(self):
        return re.match(r'(?:^|/)htmlcov/', self.name)

    def maybe_minified(self):
        return self.extname.lower() in ['.js', '.css']

    def minified_files(self):
        if self.maybe_minified() and self.lines:
            total_length = sum(len(line) for line in self.lines)
            average_length = total_length / len(self.lines)
            return average_length > 110
        else:
            return False

    def generated_go(self):
        return self.extname == ".go" and "Code generated by" in self.data

    def generated_protocol_buffer(self):
        return self.extname in self.PROTOBUF_EXTENSIONS and "Generated by the protocol buffer compiler" in self.data

    def generated_javascript_protocol_buffer(self):
        return self.extname == ".js" and "Generated by the protocol buffer compiler" in self.data

    def generated_apache_thrift(self):
        return self.extname in self.APACHE_THRIFT_EXTENSIONS and "Autogenerated by Thrift" in self.data

    def generated_jni_header(self):
        return self.extname == ".h" and "Generated from Java" in self.data

    def vcr_cassette(self):
        return self.extname == ".yml" and "VCR" in self.data

    def generated_antlr(self):
        return self.extname == ".g4" and "ANTLR" in self.data

    def generated_unity3d_meta(self):
        return self.extname == ".meta" and "Unity" in self.data

    def generated_racc(self):
        return self.extname == ".y" and "Racc" in self.data

    def generated_jflex(self):
        return self.extname == ".flex" and "JFlex" in self.data

    def generated_grpc_cpp(self):
        return self.extname == ".cc" and "GRPC" in self.data

    def generated_dart(self):
        return self.extname == ".dart" and "Generated code" in self.data

    def generated_perl_ppport_header(self):
        return self.extname == ".h" and "Perl" in self.data

    def has_source_map(self):
        if not self.maybe_minified():
            return False
        return any(re.match(r'^[/|*][\#@] source(?:Mapping)?URL|sourceURL=', l) for l in self.lines[-2:])

    def source_map(self):
        if self.extname.lower() != '.map':
            return False
        return bool(re.match(r'(\.css|\.js)\.map$', self.name)) or \
            bool(re.match(r'^{"version":\d+,', self.lines[0])) or \
            bool(re.match(r'^/\*\* Begin line maps. \*\*/{', self.lines[0]))

    def compiled_coffeescript(self):
        if self.extname != '.js':
            return False

        if re.match(r'^// Generated by ', self.lines[0]):
            return True

        if self.lines[0] == '(function() {' and \
                self.lines[-2] == '}).call(this);' and \
                self.lines[-1] == '':
            score = 0
            for line in self.lines:
                if 'var ' in line:
                    score += line.count('(_fn|_i|_len|_ref|_results)') + \
                             3 * line.count('(__bind|__extends|__hasProp|__indexOf|__slice)')
            return score >= 3

        return False

    def generated_parser(self):
        if self.extname != '.js':
            return False
        joined_lines = ''.join(self.lines[0:5])
        return bool(re.search(r'^(?:[^/]|/[^*])*/\*(?:[^*]|\*[^/])*Generated by PEG.js', joined_lines))

    def generated_net_docfile(self):
        if self.extname.lower() != ".xml" or len(self.lines) <= 3:
            return False
        return "<doc>" in self.lines[1] and "<assembly>" in self.lines[2] and "</doc>" in self.lines[-2]

    def generated_postscript(self):
        if self.extname not in ['.ps', '.eps', '.pfa']:
            return False
        return bool(re.search(r'(\n|\r\n|\r)\s*(?:currentfile eexec\s+|/sfnts\s+\[\1<)[ \t]{8,}\1', self.data)) or \
            bool(re.search(r'^%%Creator: (?:draw|mpage|ImageMagick|inkscape|MATLAB|PCBNEW|pnmtops|\(Unknown\)|Serif Affinity|Filterimage -tops)', ''.join(self.lines[0:10]))) or \
            ("EAGLE" in ''.join(self.lines[0:5]) and bool(re.search(r'^%%Title: EAGLE Drawing ', ''.join(self.lines[0:5]))))

    def generated_grammarkit(self):
        if self.extname != '.java' or len(self.lines) <= 1:
            return False
        return self.lines[0].startswith("// This is a generated file. Not intended for manual editing.")

    def generated_protocol_buffer_from_go(self):
        if self.extname != '.proto' or len(self.lines) <= 1:
            return False
        return any("This file was autogenerated by go-to-protobuf" in line for line in self.lines[:20])

    def compiled_cython_file(self):
        if self.extname not in ['.c', '.cpp'] or len(self.lines) <= 1:
            return False
        return "Generated by Cython" in self.lines[0]

    def pipenv_lock(self):
        return self.name == "Pipfile.lock"

    def generated_module(self):
        if self.extname != '.mod' or len(self.lines) <= 1:
            return False
        return "PCBNEW-LibModule-V" in self.lines[0] or "GFORTRAN module version '" in self.lines[0]

    def generated_roxygen2(self):
        if self.extname != '.Rd' or len(self.lines) <= 1:
            return False
        return "% Generated by roxygen2: do not edit by hand" in self.lines[0]

    def generated_jison(self):
        if self.extname != '.js' or len(self.lines) <= 1:
            return False
        return self.lines[0].startswith("/* parser generated by jison ") or self.lines[0].startswith("/* generated by jison-lex ")

    def generated_gamemakerstudio(self):
        if self.extname not in ['.yy', '.yyp']:
            return False

        if len(self.lines) <= 3:
            return False

        if re.search(r'"modelName"\:\s*"GM', self.lines[2]):
            return True

        if re.match(r'^\d\.\d\.\d.+\|\{', self.lines[0]):
            return True

        return False

    def generated_gimp(self):
        if self.extname not in ['.c', '.h']:
            return False

        if len(self.lines) == 0:
            return False

        pattern1 = r'/\* GIMP [a-zA-Z0-9\- ]+ C\-Source image dump \(.+?\.c\) \*/'
        pattern2 = r'/\*  GIMP header image file format \([a-zA-Z0-9\- ]+\)\: .+?\.h  \*/'

        if re.match(pattern1, self.lines[0]) or re.match(pattern2, self.lines[0]):
            return True

        return False

    def generated_html(self):
        if self.extname.lower() not in ['.html', '.htm', '.xhtml']:
            return False
        if len(self.lines) <= 1:
            return False

            # Pkgdown
        for line in self.lines[0:2]:
            if re.search(r'<!-- Generated by pkgdown: do not edit by hand -->', line):
                return True

            # Mandoc
        if len(self.lines) > 2 and self.lines[2].startswith('<!-- This is an automatically generated file.'):
            return True

            # Doxygen
        for line in self.lines[0:31]:  # 0 to 30, both inclusive
            if re.search(r'<!--\s+Generated by Doxygen\s+[.0-9]+\s*-->', line, re.I):
                return True

            # HTML tag: <meta name="generator" content="…" />
        joined_lines = ' '.join(self.lines[0:31])
        matches = re.findall(r'<meta(\s+[^>]+)>', joined_lines, re.I)
        if not matches:
            return False

        for match in matches:
            attrs = extract_html_meta(match)
            if attrs.get("name", "").lower() == 'generator':
                content_value = [attrs.get("content", ""), attrs.get("value", "")]
                for cv in content_value:
                    if cv and re.search(r'''
                            ( org \s+ mode
                            | j?latex2html
                            | groff
                            | makeinfo
                            | texi2html
                            | ronn
                            ) \b
                        ''', cv, re.I | re.X):
                        return True

        return False


def extract_html_meta(match):
    cleaned_match = re.sub(r'/\Z', "", match.strip())
    extracted_attributes = {}
    for attr in re.findall(r'(\w+)\s*=\s*("[^"]*"|\'[^\']*\'|\S+)', cleaned_match):
        key = attr[0].lower()
        value = attr[1].strip()
        if value.startswith('"') or value.startswith("'"):
            value = value[1:-1]
        extracted_attributes[key] = value
    return extracted_attributes

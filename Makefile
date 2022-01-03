install_python_dependencies:
	brew install pipenv
copy_notes: install_python_dependencies
	cd _operations && pipenv install && pipenv run python3 copy_notes.py ${CONFIG}

install_runtime_dependencies:
	brew install rbenv && gem install bundler jekyll && bundle install

start: install_runtime_dependencies
	bundle exec jekyll serve
import mimetypes
import os

from flask import Flask, jsonify, send_file, Response
import importlib.resources
import zipfile

from dataset_sh.io import DatasetStorageManager


def load_frontend_assets(prefix='build/'):
    frontend_assets = {}
    with importlib.resources.path("dataset_sh.assets", 'app-ui.frontend') as asset_zip_path:
        if os.path.exists(asset_zip_path):
            with zipfile.ZipFile(asset_zip_path, 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    if file_info.is_dir():
                        continue
                    if file_info.filename.startswith(prefix):
                        with zip_ref.open(file_info) as file:
                            file_content = file.read()
                            frontend_assets[file_info.filename[len(prefix):]] = file_content
    return frontend_assets


def create_app(manager=None, frontend_assets=None):
    if manager is None:
        manager = DatasetStorageManager()
    app = Flask(__name__, static_folder=None)

    @app.route('/api/dataset', methods=['GET'])
    def list_datasets():
        items = manager.list_datasets()
        return jsonify(items.model_dump(mode='json')), 200

    @app.route('/api/store', methods=['GET'])
    def list_stores():
        items = manager.list_dataset_stores()
        return jsonify(items.model_dump(mode='json')), 200

    @app.route('/api/dataset/<store_name>', methods=['GET'])
    def list_datasets_in_store(store_name):
        items = manager.list_datasets_in_store(store_name)
        return jsonify(items.model_dump(mode='json')), 200

    @app.route('/api/dataset/<store_name>/<dataset_name>/readme', methods=['GET'])
    def get_dataset_readme(store_name, dataset_name):
        return manager.get_dataset_readme(store_name, dataset_name), 200

    @app.route('/api/dataset/<store_name>/<dataset_name>/remote-source', methods=['GET'])
    def get_dataset_remote_source(store_name, dataset_name):
        source = manager.get_dataset_source_info(store_name, dataset_name)
        return jsonify(source.model_dump(mode='json')), 200

    @app.route('/api/dataset/<store_name>/<dataset_name>/meta', methods=['GET'])
    def get_dataset_meta(store_name, dataset_name):
        return jsonify(manager.get_dataset_meta(store_name, dataset_name)), 200

    @app.route('/api/dataset/<store_name>/<dataset_name>/collection/<collection_name>/sample', methods=['GET'])
    def get_collection_sample(store_name, dataset_name, collection_name):
        sample = manager.get_sample(store_name, dataset_name, collection_name)
        return jsonify(sample), 200

    @app.route('/api/dataset/<store_name>/<dataset_name>/collection/<collection_name>/code', methods=['GET'])
    def get_collection_code(store_name, dataset_name, collection_name):
        code = manager.get_usage_code(store_name, dataset_name, collection_name)
        return {'code': code}, 200

    @app.route('/api/dataset/<store_name>/<dataset_name>/file', methods=['GET'])
    def get_dataset_file(store_name, dataset_name):
        return send_file(
            manager.get_dataset_file_path(store_name, dataset_name),
            as_attachment=True,
            download_name=f"{store_name}_{dataset_name}.dataset"
        )

    index_html_file = 'index.html'

    @app.route('/', defaults={'path': ''})
    @app.route("/<string:path>")
    @app.route('/<path:path>')
    def catch_all(path):
        fp = path
        if fp not in frontend_assets:
            # due to frontend routing, we need to serve content index.html of non static asset url.
            if index_html_file not in frontend_assets:
                return '', 404
            fp = index_html_file

        mime_type, _ = mimetypes.guess_type(fp)
        content_bytes = frontend_assets[fp]
        if mime_type is None:
            mime_type = 'application/octet-stream'
        return Response(content_bytes, content_type=mime_type)

    return app


DISABLE_UI = os.environ.get('DISABLE_DATASET_APP_UI', '0') != '0'

_frontend_assets = {
    'build/index.html': "dataset.sh web ui is disabled"
}

if not DISABLE_UI:
    _frontend_assets = load_frontend_assets()

app = create_app(frontend_assets=_frontend_assets)

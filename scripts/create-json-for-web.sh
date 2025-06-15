#!/bin/bash -ue
# PDFからWeb表示用のJSONを作成するスクリプト
#
# 使用方法:
#   ./scripts/create-json-for-web.sh [-w work_dir] pdf_path output_json_path
#
# 使用例:
#   ./scripts/create-json-for-web.sh hoge.pdf ./public/reports/hoge.json
#
# パラメータ:
#   pdf_path: PDFファイルのパス
#   output_json_path: 出力JSONファイルのパス
#
# オプション:
#   -w work_dir: 作業ディレクトリを指定する (デフォルト: 一時ディレクトリ)

# check if poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "poetry could not be found"
    exit 1
fi

# cd to parent directory of this script
cd $(dirname $(dirname $(realpath $0)))

work_dir=
while getopts "w:" opt; do
    case $opt in
        w) work_dir=$OPTARG ;;
        *) echo "Usage: $0 [-d work_dir] <pdf_path> <output_json_path>" ;;
    esac
done
shift $((OPTIND - 1))

pdf_path=$1
output_json_path=$2

if [[ -z "$work_dir" ]]; then
    work_dir=$(mktemp -d)
fi

tmpdir_image=$work_dir/images
tmpdir_json=$work_dir/jsons
echo "images dir: $tmpdir_image"
echo "json dir: $tmpdir_json"

# PDF => Images
echo python tools/pdf_to_images.py -o $tmpdir_image $pdf_path
python tools/pdf_to_images.py -o $tmpdir_image $pdf_path
# Images => JSON Files
python tools/analyze_image.py -i $tmpdir_image -o $tmpdir_json
# JSON Files => Merged JSON File
merge_json_file=$work_dir/merged.json
python tools/merge_jsons.py -i $tmpdir_json -o $merge_json_file

# Merged JSON File => JSON File for Web
npx tsx data/converter.ts -i $merge_json_file -o $output_json_path --ignore-errors

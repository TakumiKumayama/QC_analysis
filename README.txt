<<<<<<< HEAD
[HV_LV_TEST]
▶︎ スクリプト概要
- atlasdb01.kek.jp上で使用する。pullするディレクトリの指定はない。
- HV_LV_TESTの結果を扱う時の単位は全て[mOhm]と[nA]で統一させている。
- スプレッドシートを参照し、品質検査が終了したフレキシブル基板の一覧リスト(シリアルナンバー)を作成。
- 作成したリストを元に、ローカルデータベースから試験結果jsonファイルを取得。
- -pのオプションをつけることでヒストグラムの作成も可能。

▶︎ ファイル構造
- scripts
    - get_json.py       スプレッドシートの参照 & データベースからjson取得 & 結果の一覧をHV_LV_TEST.txtにまとめる。
    - localDBtools.py   ローカルデータベースからデータ取得するためのクラス。get_json.py内で使用する。
    - mkhist.py         get_json.pyで作成したHV_LV_TEST.txtを参照し、ヒストグラムを作成。get_json.pyに-pオプションをつけることで動かせる。
- data
    - img               mkhist.pyで作成したヒストグラム(HV_LV_TEST.pdf)を格納。
    - json              ローカルデータベースから取得したフレキシブル基板ごとの試験結果(20UPGPQXXXYYYY.json)を個別に格納。
    - lists             スプレッドシートを参照し、作成したシリアルナンバーのリスト(PCB.txt)を格納。
    - results           取得した結果の一覧をHV_LV_TEST.txtにまとめて格納。

▶︎ コードの実行
コードの実行 HV_LV_TEST/scripts にて以下のコマンドを実行。
python3  get_json.py

オプションをつけることも可能。
- -p : プロットの作成。get_json.py内でmkhist.cppを呼び出す。
    python3 get_json.py -p

- -v : デバッグ用。localDBtools.py内での挙動を追うときの使用を推奨する。ローカルデータベースの環境が変わったタイミングなど。
    python3 get_json.py -v


###################################################################################################################

[LAYER_THICKNESS]
▶︎ スクリプト概要
- atlasdb01.kek.jp上で使用する。pullするディレクトリの指定はない。
- Layer Thicknessの結果を扱う時の単位は全て[um]で統一させている。
- スプレッドシートを参照し、品質検査が終了したフレキシブル基板の一覧リスト(シリアルナンバー)を作成。
- 作成したリストを元に、ローカルデータベースから試験結果jsonファイルを取得。
- -pのオプションをつけることでヒストグラムの作成も可能。

▶︎ ファイル構造
- scripts
    - get_json.py       スプレッドシートの参照 & データベースからjson取得 & 結果の一覧をLayerThickness.txtにまとめる。
    - localDBtools.py   ローカルデータベースからデータ取得するためのクラス。get_json.py内で使用する。
    - mkhist.py         get_json.pyで作成したLayerThickness.txtを参照し、ヒストグラムを作成。get_json.pyに-pオプションをつけることで動かせる。
- data
    - img               mkhist.pyで作成したヒストグラム(LayerThickness.pdf)を格納。
    - json              ローカルデータベースから取得したフレキシブル基板ごとの試験結果(20UPGPQXXXYYYY.json)を個別に格納。
    - lists             スプレッドシートを参照し、作成したシリアルナンバーのリスト(PCB.txt)を格納。
    - results           取得した結果の一覧をLayerThickness.txtにまとめて格納。

▶︎ コードの実行
コードの実行 LAYER_THICKNESS/scripts にて以下のコマンドを実行。
python3  get_json.py

オプションをつけることも可能。
- -p : プロットの作成。get_json.py内でmkhist.cppを呼び出す。
    python3 get_json.py -p

- -v : デバッグ用。localDBtools.py内での挙動を追うときの使用を推奨する。ローカルデータベースの環境が変わったタイミングなど。
    python3 get_json.py -v


###################################################################################################################
[MODULE_IV]
!!注意!!
- このスクリプトのみrepicgw環境下での操作を想定しています。
- スプレッドシートを参照し、アセンブリが完了したモジュールのリストを作成。
- リスト内のモジュールIV(INITIAL_WARM)のjsonファイルを取得。
- 取得したjsonファイルはatlasdb01.kek.jpへsshすることで、Module, BareModule, sensorの各製造工程のIVを比較できるようになります。
- BAREMODULE_SENSOR_IV/data/json/Module/以下にscpしてもらう想定で作成している。
- repicgw以下で作業をしたい場合は各自開発を推奨します。

▶︎ ファイル構造
- scripts
    - get_json.py       スプレッドシートの参照 & データベースからjson取得 & 結果の一覧を.txtにまとめる。
    - localDBtools.py   ローカルデータベースからデータ取得するためのクラス。get_json.py内で使用する。
- data
    - lists             スプレッドシートを参照し、作成したシリアルナンバーのリスト(Module.txt)を格納。
    - json              
       - Module         ローカルデータベースから取得したモジュールのIV試験結果(20UPGMXXXYYYY.json)を個別に格納。
       
       
▶︎ コードの実行
コードの実行 LAYER_THICKNESS/scripts にて以下のコマンドを実行。
python3  get_json.py

- -v : デバッグ用。localDBtools.py内での挙動を追うときの使用を推奨する。ローカルデータベースの環境が変わったタイミングなど。
    python3 get_json.py -v








[BAREMODULE_SENSOR_IV]
▶︎ スクリプト概要
- atlasdb01.kek.jp上で使用する。pullするディレクトリの指定はない。
- BareModule, sensorのIVを扱う時の単位は全て[V]と[uA]で統一させている。
- スプレッドシートを参照し、アセンブリが完了したModule-BareModule-sensorのリストを作成。
- 作成したリストを元に、ローカルデータベースから試験結果jsonファイルを取得。
- -pのオプションをつけることでヒストグラムの作成も可能。ただし、-pオプションをつける前にrepicgwからModuleのIV結果を持ってくる必要がある。

▶︎ 結果の出力方法
- get_jsonに-pのオプションをつけるとsensor, BareModule, Moduleの角製造工程におけるIVの比較プロットが作成される。※ただし、repicgwからModuleのjsonを所定のディレクトリにscpしてくる必要がある。詳細は[MODULE_IV]を参照。
- ModuleとBareModuleのIVに関する品質検査に関しては、２つの品質基準を要求する(2025.3.25時点。変更の可能性有)。
- get_jsonに-pのオプションをつけると以下二つのクライテリアに基づいたModuleの品質結果がresults/Module_Judge_result.listに作成される。

▶︎ 品質基準 *2025/3時点のもの。今後変更の可能性あり。
- ① I_{module, baremodule} < 2I_{sensor} @V_{dep}+50V
    全空乏化電圧(70V)+50V地点におけるModuleおよびBareModuleの電流量がsensor単体時の電流量の2倍より低い値を示すことを課している。この品質基準を品質基準1としている。

- ② I_{module, baremodule}[uA/cm^2] <  0.75 @V_{dep}+50V
    全空乏化電圧(70V)+50V地点におけるModuleおよびBareModuleの単位面積あたりの電流量が0.75 uA/mm^2より低い値を示すことを課している。この品質基準を品質基準2としている。

▶︎ ファイル構造
- scripts
    - get_json.py       スプレッドシートの参照 & データベースからjson取得。-pオプションをつけると、プロットの作成 & 品質基準に基づいたリスト(results/Module_Judge_result.list)を作成。
    - localDBtools.py   ローカルデータベースからデータ取得するためのクラス。get_json.py内で使用する。
- data
    - img               Module BareModule sensorの各工程におけるIV比較のプロットをModuleのSNごとに作成し格納(20UPGMXXXXYYYY.pdf)。get_json.pyに-pオプションをつけることで作成可能。
    - lists             スプレッドシートを参照し、作成したシリアルナンバーのリスト(BareModule.txt)を格納。
                        sensor BareModule Moduleのシリアルナンバーの一覧(Module_Bare_sensor.txt)も作成し、ここに格納。
    - results           品質基準に基づいたリスト(results/Module_Judge_result.list)を格納。
    - json              
       - Module         repicgwからModuleのjsonをscpしてくる。
       - BareModule     ローカルデータベースから取得したBareModuleの試験結果(20UPGBXXXYYYY.json)を個別に格納。
       - sensor         ローカルデータベースから取得したsensorの試験結果(20UPGSXXXYYYY.json)を個別に格納。
       
▶︎ コードの実行
コードの実行 LAYER_THICKNESS/scripts にて以下のコマンドを実行。
python3  get_json.py

オプションをつけることも可能。
- -p : IVカーブプロットの作成。品質基準に基づいた一覧リスト(results/Module_Judge_result.list)を作成。
    python3 get_json.py -p

- -v : デバッグ用。localDBtools.py内での挙動を追うときの使用を推奨する。ローカルデータベースの環境が変わったタイミングなど。
    python3 get_json.py -v
=======
ちょっと変更
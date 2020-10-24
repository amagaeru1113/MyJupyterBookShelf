# 2020年のベストな文書類似度アルゴリズム：初心者ガイド

**これは投稿記事([The Best Document Similarity Algorithm in 2020: A Beginner’s Guide](https://towardsdatascience.com/the-best-document-similarity-algorithm-in-2020-a-beginners-guide-a01b9ef8cf05), Author [Masatoshi Nishimura](https://medium.com/@Massanishi?source=post_page-----a01b9ef8cf05--------------------------------))の自分用翻訳です。
DeepL翻訳を多用します。**

## The Best Document Similarity Algorithm in 2020: A Beginner’s Guide
 Picking the winner from 5 popular algorithms based on an experiment

---

2020年の文書類似性タスクに関する最高のアルゴリズムを知りたいなら、あなたは正しい場所に来ています。

33,914のニューヨークタイムズの記事で、私は文書の類似性の品質のための5つの人気のあるアルゴリズムをテストしました。それらは伝統的な統計的アプローチから現代的なディープラーニングのアプローチまで多岐にわたっています。

それぞれの実装は50行以下のコードです。そして、使用されているモデルはすべてインターネットから取得しています。そのため、同様の結果を期待しながら、データサイエンスの予備知識がなくても、すぐに使用することができるようになります。

この投稿では、各アルゴリズムをどのように使い、最適なものを選ぶ方法を学びます。以下はアジェンダです。

1. Defining the best:
2. Experiment goal statement:
3. Data setup
4. Comparison 
5. Algorithm setup:
6. Picking the winner:
7. Seuggestion for starters:

あなたが自然言語処理やAIに手を出したい、関連性のある提案でユーザー体験にスパイスを与えたい、古い既存のアルゴリズムをアップグレードしたいと考えている場合、この記事は最適です。

### Data Scientists Argue For The Absolute Best
あなたは「最高の文書類似性アルゴリズム」という用語を検索することにしました。

すると、学術論文、ブログ、Q&Aなどの検索結果が表示されます。特定のアルゴリズムのチュートリアルに焦点を当てたものもあれば、理論的な概要に焦点を当てたものもあります。

学術論文の見出しには、このアルゴリズムは80%の精度で75%しか達成していない他のすべてのアルゴリズムを打ち負かしたと書かれています。いいでしょう。しかし、その違いは、私たちの目には顕著に見えるようにするのに十分なのでしょうか？2%の増加についてはどうでしょうか? そのアルゴリズムを実装するのはどのくらい簡単なのでしょうか？科学者達は、実用的な意味合いを除いて、与えられたテストセットの中で最高のものを求めて行くことに偏っています。

System | MultiNLI | Question NLI | SWAG
BERT | 86.7 | 91.1 | 86.3
OpenAI GPT(Prev. SOTA) | 82.2 | 88.1 | 75.0

Q&Aでは、誇大妄想マニアが会話を支配しています。今日の最高のアルゴリズムはBERTだと言う人もいます。そのアルゴリズムのコンセプトは、他のすべてのものを打ち負かすほどの革命的なものです。一方、皮肉屋は、すべては仕事に依存していると言う。いくつかの答えは、ディープラーニングを先取りした数年前のものです。この[Stackoverflow](https://stackoverflow.com/questions/8897593/how-to-compute-the-similarity-between-two-text-documents)を見てみましょう。最も投票されたのが2012年に書かれたとき、それが本当に私たちにとって何を意味しているのかを判断するのは難しいでしょう。

Googleは、検索を1%改善するためだけに、何百万ドルものエンジニアパワーと最新の計算能力を投入して喜んでいるだろう。それはおそらく実用的ではないだろうし、私たちにとっても意味のあることではないだろう。

性能の向上と実装に必要な技術的な専門知識のトレードオフは何ですか？どのくらいのメモリを必要としますか？最小限の前処理でどれくらいの速度で実行できるか？

あなたが見たいのは、あるアルゴリズムが実用的な意味で他のアルゴリズムよりも優れているということです。

この記事はあなたがの文書類似度問題のための道具として、どのアルゴリズムが良いかのガイドラインを示します。



### Diverse algorithms, full-length popular articles, pretrained models
この実験でのゴールは四つです。

1. 同じデータセット上で複数のアルゴリズムを実行することで、どのアルゴリズムが他のアルゴリズムとどの程度の差があるのかを知ることができます。
2. 人気のあるメディアの記事をデータセットとして使用することで、実際のアプリケーションの有効性を発見することができます。
3. 記事のURLにアクセスすることで、結果の質の違いを比較することができます。
4. 公開されている事前学習済みのモデルのみを使用することで、独自の文書類似度を設定し、類似した出力を期待することができます。

>"事前学習モデルはあなたの味方" <br>
> \- Cathal Horan, machine learning engineer at Intercom


### Data Setup — 5 base articles

この実験では、ニューヨーク・タイムズの記事33,914本を選びました。それらは2018年から2020年6月までのものです。データは、ほとんどがフルコンテンツで解析されたRSSフィードから収集されています。記事の平均長さは6,500文字です。

そのプールから、類似性検索の基準として5つを選びました。それぞれが異なるカテゴリーを表しています。

意味的なカテゴリの上に、我々は同様に書かれたフォーマットを測定します。より詳細な説明は以下の通りです。


1. [How My Worst Date Ever Became My Best](https://www.nytimes.com/2020/02/14/style/modern-love-worst-date-of-my-life-became-best.html) (Lifestyle, Human Interest)
2. [A Deep-Sea Magma Monster Gets a Body Scan](https://www.nytimes.com/2019/12/03/science/axial-volcano-mapping.html) (Science, Informational)
3. [Renault and Nissan Try a New Way After Years When Carlos Ghosn Ruled](https://www.nytimes.com/2019/11/29/business/renault-nissan-mitsubishi-alliance.html) (Business, News)
4. [Dominic Thiem Beats Rafael Nadal in Australian Open Quarterfinal](https://www.nytimes.com/2020/01/29/sports/tennis/thiem-nadal-australian-open.html) (Sports, News)
5. [2020 Democrats Seek Voters in an Unusual Spot: Fox News](https://www.nytimes.com/2019/04/17/us/politics/fox-news-democrats-2020.html) (Politics, News)

### Judgment Criteria
5つの基準で類似性の本質を判断します。結果を見たいだけの方はここを飛ばしてください。

1. タグオーバーラップ
2. セクション
3. サブセクション
4. ストーリースタイル
5. テーマ

タグは、コンテンツの類似性における人間の判断に最も近い代理人である。ジャーナリスト自身が手書きでタグを書き留めています。HTMLヘッダのnews_keywordsメタタグで調べることができます。タグを使う一番の利点は、2つのコンテンツがどれだけ重複しているかを客観的に測定できることです。それぞれのタグのサイズは1から12まであります。2つの記事の重複が多ければ多いほど、似ているということになります。

第二に、セクションを見ます。これは、ニューヨークタイムズがどのように記事を最高レベルで分類しているかを示しています：科学、政治、スポーツなど。URLの最初の部分は、ドメイン（nytimes.com/...）の直後にセクション（またはスラッグ）を表示します。

3つ目は小節です。例えば、オピニオンセクションはworldに細分化されていたり、worldはオーストラリアに細分化されていたりします。すべての記事に含まれているわけではありませんし、他の2つほどの意味はありません。

4つ目は、文体です。文書比較の分析の多くは、意味論だけを見ています。しかし、実用的なユースケースでレコメンデーションを比較しているので、同じような書き方をしたいと考えています。例えば、学術誌の「ランニングシューズと装具」の直後に、「ランニングシューズのトップ10」という商業的にフォーカスした読み物を手に入れたいわけではありません。[ジェファーソンカントリースクール](http://seduc.csdecou.qc.ca/sec-anglais/files/2015/01/MS_FeatArtWrtgPerRdg.pdf)で教えられている執筆ガイドラインに基づいて記事をグループ化します。リストは、人間の興味、性格、ベスト（ex:製品レビュー）、ニュース、ハウツー、過去の出来事、情報に従う。

### 5 Algorithm Candidates

アルゴリズムが以下のものが対象です。

1. Jaccard
2. TF-IDF
3. Doc2vec
4. USE
5. BERT

それぞれのアルゴリズムは、33,914記事に対して実行され、最も高いスコアを持つトップ3の記事を見つけた。このプロセスは、ベースとなる記事のそれぞれに対して繰り返されます。

入力は記事の内容を全文で入力しました。タイトルは無視されました。

アルゴリズムの中には、文書の類似性を考慮して作られていないものもあるので注意が必要です。しかし、インターネット上ではこのように多様な意見があるので、私たちは自分の目で結果を見てみましょう。

私たちは概念的な理解や詳細なコードレビューに焦点を当てていません。むしろ目的は、セットアップがいかに簡単かを示すことです。ここで説明されているすべての詳細を理解していなくても心配しないでください。ポストに沿って進むことは重要ではありません。理論を理解するために、他の人が書いた優れたブログを読むために、下の方にある読書リストをチェックしてください。

You can find the entire codebase in the [Github repo](https://github.com/massanishi/document_similarity_algorithms_experiments).



#### Jaccard 

ポール・ジャカードは[1世紀以上前](https://en.wikipedia.org/wiki/Paul_Jaccard)にこの式を提案しました。そしてこの概念は長い間類似性タスクの標準的な手段となってきました

幸いなことに、ジャカードが最も理解しやすいアルゴリズムであることがわかります。ベクトル化されていないので、数学は簡単です。そして、ゼロからコードを書くことができます。

また、jaccardは余弦類似度を使用しない数少ないアルゴリズムの一つです。単語をトークン化し、和にまたがる交点を計算する。
テキストの前処理にはNLTKを使用しています。

ステップ
1. 全文章を小文字化
2. トークン化
3. ストップワードの除去
4. 句読点の除去
5. 2つの書類で交点・結合を計算

コード
```
def calculate_jaccard(word_tokens1, word_tokens2):
	# Combine both tokens to find union.
	both_tokens = word_tokens1 + word_tokens2
	union = set(both_tokens)

	# Calculate intersection.
	intersection = set()
	for w in word_tokens1:
		if w in word_tokens2:
			intersection.add(w)

	jaccard_score = len(intersection)/len(union)
	return jaccard_score
```

#### TF-IDF

これも[1972年](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)からある、確立されたアルゴリズムです。何十年にもわたって十分なテストが行われており、Elasticsearchのデフォルトの検索実装となっています。

Scikit-learnはTF-IDFの素晴らしい実装を提供しています。TfidfVectorizerは誰でも一瞬でこれを試すことができます。

TF-IDFの単語ベクトルの結果は、scikit-learnの余弦類似度によって計算されます。残りの例では、この余弦類似度を使用します。コサイン類似度は多くの機械学習タスクで使われるほど重要な概念なので、慣れ親しんでおくと良いかもしれません（[学術的な概要](https://www.sciencedirect.com/topics/computer-science/cosine-similarity)）。

コード
```
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def process_tfidf_similarity():
	vectorizer = TfidfVectorizer()

	# To make uniformed vectors, both documents need to be combined first.
	documents.insert(0, base_document)
	embeddings = vectorizer.fit_transform(documents)

	cosine_similarities = cosine_similarity(embeddings[0:1], embeddings[1:]).flatten()

```

#### Doc2vec
Word2vecは2014年に登場し、当時の開発者の息の根を止めた。有名なデモを聞いたことがある人もいるかもしれません。

> King - Man == Queen

Word2vecは個々の単語を理解するのに優れていますが、文章全体をベクトル化するには時間がかかります。文書全体のベクトル化はおろか、文書全体のベクトル化にも時間がかかります。

代わりに、各単語の代わりに段落をベクトル化する類似の埋め込みアルゴリズムであるDoc2vecを使用します（[2014年、Google Inc](https://cs.stanford.edu/~quocle/paragraph_vector.pdf)). より消化しやすい形では、Gidi Shperber氏による[イントロブログ](https://medium.com/wisio/a-gentle-introduction-to-doc2vec-db3e8c0cce5e)をご覧ください。

Doc2vecでは、残念ながら法人協賛のプリトレーニングモデルは公開されていません。そこで、[このリポジトリ](https://github.com/jhlau/doc2vec)にある事前学習済みのenwiki_dbowモデルを使用します。英語版ウィキペディア（不特定多数ですが、モデルサイズは1.5GBとまともです）で学習されています。

Doc2vecの公式ドキュメントには、どれだけの長さの入力を挿入しても良いと書かれています。トークン化されたら、gensim ライブラリを使ってドキュメント全体を投入します。

コード
```
from gensim.models.doc2vec import Doc2Vec

def process_doc2vec_similarity():

	filename = './models/enwiki_dbow/doc2vec.bin'
	model= Doc2Vec.load(filename)

	tokens = preprocess(base_document)

	# Only handle words that appear in the doc2vec pretrained vectors. enwiki_ebow model contains 669549 vocabulary size.
	tokens = list(filter(lambda x: x in model.wv.vocab.keys(), tokens))
	base_vector = model.infer_vector(tokens)
```


#### Universal Sentence Encoder (USE)

[2018年5月](https://arxiv.org/abs/1803.11175)にGoogleがかなり最近発表した人気のアルゴリズムです（この発表の背景には有名なレイ・カーツワイル氏がいました🙃）。実装の詳細は[GoogleのTensorflow](https://www.tensorflow.org/hub/tutorials/semantic_similarity_with_tf_hub_universal_encoder)に詳しく書かれています。

今回はGoogleの最新の公式プレトレーニング済みモデルを使用します。[Universal Sentence Encoder 4](https://tfhub.dev/google/universal-sentence-encoder/4)です。

その名の通り、文章を意識して作られています。しかし、公式文書では入力サイズに制約はありません。文書の比較作業に使うのを止めるようなことは何もありません。

ドキュメント全体をそのままTensorflowに挿入します。トークン化は行いません。

コード
```
import tensorflow_hub as hub

def process_use_similarity():
	filename = "./models/universal-sentence-encoder_4"
	model = hub.load(filename)

	base_embeddings = model([base_document])

	embeddings = model(documents)

	scores = cosine_similarity(base_embeddings, embeddings).flatten()
```

#### Bidirectional Encoder Representations from Transformers (BERT)

これは大物ですね。Googleは[2018年11月](https://ai.googleblog.com/2018/11/open-sourcing-bert-state-of-art-pre.html)にBERTアルゴリズムをオープンソース化した。翌年、Googleの検索担当副社長は、過去5年間で最大の飛躍を遂げたBERTと称した[ブログ記事](https://blog.google/products/search/search-language-understanding-bert/)を公開しました。

これは、検索クエリを理解するために特別に構築されています。一文の文脈を理解することに関しては、BERTはここで言及されている他のすべてのものを凌駕しているようです。

元々のBERTタスクは、大量のテキスト入力を扱うことを意図したものではありませんでした。複数文の埋め込みには、計算速度が優れているUKPLab（ドイツ大学）が公開している[Sentence Transformers](https://github.com/UKPLab/sentence-transformers)というオープンソースのプロジェクトを使用する。また、[元のモデルと同等の事前学習済みモデル](https://github.com/UKPLab/sentence-transformers#performance)も提供してくれます。

そこで、各文書は文にトークン化されます。そして、その結果を平均化して1つのベクトルで文書を表現します。

コード
```
from sentence_transformers import SentenceTransformer

def process_bert_similarity():
	# This will download and load the pretrained model offered by UKPLab.
	model = SentenceTransformer('bert-base-nli-mean-tokens')

	sentences = sent_tokenize(base_document)
	base_embeddings_sentences = model.encode(sentences)
	base_embeddings = np.mean(np.array(base_embeddings_sentences), axis=0)
```

### Winner Algorithms
5つの異なるタイプの記事について、それぞれのアルゴリズムがどのように機能するか見てみましょう。比較のために、スコアの高い記事の上位3つを選択します。

このブログ記事では、5つの記事のそれぞれについて、最もパフォーマンスの高いアルゴリズムの結果のみを見ていきます。個々の記事へのリンクとともに、完全な結果については、[レポジトリ](https://github.com/massanishi/document_similarity_algorithms_experiments)のアルゴリズムディレクトリを参照してください。

#### 1. [How My Worst Date Ever Became My Best](https://www.nytimes.com/2020/02/14/style/modern-love-worst-date-of-my-life-became-best.html)
BERTの勝ち。

記事は、50代のバツイチ女性の恋愛デートを題材にした人情話。

この文体では、有名人の名前のような特定の名詞は載せません。時期的なものでもありません。2010年からの1つの人間の関心事の話は、今日と同じように関連性がある可能性が高いでしょう。したがって、比較において、1つのアルゴリズムが大きく外れているわけではありませんでした。

それはUSEとの接戦だった。USEのストーリーがLGBTQなどの社会問題に遠回りしたのに対し、BERTは恋愛やデートにのみ焦点を当てていました。他のアルゴリズムは、おそらく「元夫」という言葉を見たことから、家族や子供に関する話題に分岐しました。




Table:BERT Results For The 1st Article (dating) — Document Similarity Experiment

| Title | Tag Overlap | Section Overlap | Subsection Overlap | Style Overlap | Theme | Subjective |
|:-----------:|:------------|:------------|:------------|:------------|:------------|:------------|
| [Why Are All the Exes Texting?](https://www.nytimes.com/2020/05/29/style/modern-love-coronavirus-why-are-all-the-exes-texting.html) | 1      | Y         | Y | Y | Dating | Related |
| [When Love Seems Too Easy to Trust](https://www.nytimes.com/2018/04/13/style/when-love-seems-too-easy-to-trust.html) | 1      | Y         | Y | Y | Dating | Related |
| [He Saved His Last Lesson for Me](https://www.nytimes.com/2020/03/06/style/modern-love-long-distance-dating-korea.html) | 1      | Y         | Y | Y | Dating | Related |

#### 2. [A Deep-Sea Magma Monster Gets a Body Scan](https://www.nytimes.com/2019/12/03/science/axial-volcano-mapping.html)

TF-IDFの勝利。

この科学論文は、海の中の活火山を3Dスキャンすることについて語っています。

3Dスキャン、火山、海洋というのは珍しい用語なので、簡単に手に取ることができます。すべてのアルゴリズムがうまくいっています。

TF-IDFは、地球の海の中の火山の話しかしないものを正しく選んでいました。USEは海洋ではなく火星の火山に焦点を当てており、同様に良い候補となった。また、ロシアの軍用潜水艦についての記事は、科学とは関係がなく、話題から外れているものをピックアップしています。

Tabl:TF-IDF Results For The 2nd Article (volcano) — Document Similarity Experiment

Title | Tag Overlap | Section Overlap | Subsection Overlap | Style Overlap | Theme | Subjective
--- | --- | --- | --- | --- | --- | ---
[A 3D Encounter With a Violent Volcano’s Underbelly](https://www.nytimes.com/2019/12/18/science/volcano-3d-reunion-island.html) | 4 | Y | N | Y | 3D Mapped Volcano | Highly Related
[Pressure, and Mystery, on the Rise](https://www.nytimes.com/2015/01/06/science/predicting-what-a-volcano-may-or-may-not-do-is-as-tricky-as-it-is-crucial-as-iceland-well-knows.html) | 1 | Y | Y | Y | Icelands's Volcano | Related
[It’s Not Just Hawaii: The U.S. Has 169 Volcanoes That Could Erupt](https://www.nytimes.com/2018/05/14/us/us-active-volcanoes-hawaii.html) | 2 | N | N | Y | Volcanos | Related

#### 3. Renault and Nissan Try a New Way After Years When Carlos Ghosn Ruled
TF-IDFが勝利。

カルロス・ゴーン前CEOが脱走した後、ルノーと日産に何が起こったのかが語られています。

理想的な試合は、この3つのエンティティについて話すことでしょう。前の2つの記事に比べて、この記事ははるかにイベント駆動型で、時間に敏感です。関連するニュースは、この日に似たようなことが起こるはずです（2019年11月からです）。

TF-IDFは、日産のCEOに焦点を当てた記事を正しく選んだ。他の人は、フィアット・クライスラーとプジョーの提携など、一般的な自動車業界のニュースについて話している記事を選んでいました。

また、Doc2vecとUSEがまったく同じ結果につながったことも注目に値する。


Table:TF-IDF Results For The 3rd Article (Nissan) — Document Similarity Experiment

|Title|Tag Overlap|Section Overlap|Subsection Overlap|Style Overlap|Theme|Subjective|
|---|---|---|---|---|---|---|
| [Nissan CEO Says 'No Merit' in Merger With Renault-Nikkei](https://www.nytimes.com/reuters/2018/04/25/business/25reuters-renault-nissan-m-a.html) | 3 | N | N | Y | Nissan and Renault | Related |
| [Carlos Ghosn and the Roots of Nissan’s Decline](https://www.nytimes.com/2020/01/15/automobiles/nissan-carlos-ghosn-strategy.html) | 3 | N | N | N | Carlos Ghosn | Related |
| [Renault Chooses Volkswagen Executive as New C.E.O.](https://www.nytimes.com/2020/01/28/business/renault-ceo-luca-de-meo.html) | 5 | Y | Y | Y | Renault CEO | Very Related |


#### 4. Dominic Thiem Beats Rafael Nadal in Australian Open Quarterfinal
ジャカード、TF-IDF、USEの間で同点。

2020年の全豪オープン（テニスの試合）に出場するテニスプレーヤーのドミニク・ティエム選手についての記事です。

ニュースはイベントドリブンであり、個人に非常に特化しています。そのため、理想的にはドミニクと全豪オープンについての試合になります。

残念ながら、結果は十分なデータがないために苦しんだ。すべてテニスの話をしていました。しかし、いくつかの試合は、2018年から全仏オープンのドミニクについて話していた。または、全豪オープンからロジャー・フェデラーについてでした。

結果は3つのアルゴリズムの間で同点となりました。このことが重要なことを物語っています: 最高の類似性マッチングの結果を得るためには、データプールの収集、多様化、拡張に最善を尽くす必要があります。


Table:Jaccard Results For The 4th Article (tennis) — Document Similarity Experiment

|Title|Tag Overlap|Section Overlap|Subsection Overlap|Style Overlap|Theme|Subjective|
|---|---|---|---|---|---|---|
| [Djokovic vs. Federer, a Rivalry for the Ages, Is One-Sided This Time](https://www.nytimes.com/2020/01/30/sports/tennis/djokovic-federer-australian-open.html) | 3 | Y | Y | Y | Australian Open | Related |
| [Novak Djokovic Wins the Australian Open](https://www.nytimes.com/2020/02/02/sports/tennis/australian-open-djokovic-thiem.html) | 4 | Y | Y | Y | Dominic vs Novak in Australian Open | Very Related |
| [With Rome Title, Nadal Back on Track Entering French Open](https://www.nytimes.com/aponline/2018/05/20/sports/tennis/ap-ten-italian-open.html) | 1 | N | N | Y | French Open | Unrelated |


#### 5. 2020 Democrats Seek Voters in an Unusual Spot: Fox News
USEが勝利。

2020年の選挙に向けてフォックスニュースに登場するバーニー・サンダースを中心とした民主党の記事です。

それぞれの話題は、それだけで大きなものになります。民主党候補と選挙に関する記事が豊富です。話の要旨が斬新なので、民主党候補とフォックスの関係を論じたものを優先しました。

余談ですが、実際には政治の世界での提案には気をつけたいものです。リベラルと保守的なニュースを混ぜると、読者を簡単に動揺させることができます。我々はニューヨークタイムズだけを相手にしているので、それは我々の関心事ではないでしょう。

USEでは、バーニー・サンダースやFox、MSNBCなどのテレビケーブルについて語った記事を見つけました。他には、2020年の選挙で他の民主党候補者を論じている記事を選んだ。これらはあまりにも一般的と考えられていた。


Table:USE Results For The 5th Article (Fox) — Document Similarity Experiment

|Title|Tag Overlap|Section Overlap|Subsection Overlap|Style Overlap|Theme|Subjective|
|---|---|---|---|---|---|---|
| [Bernie Sanders Had a Problem With MSNBC. Then Came Super Tuesday.](https://www.nytimes.com/2020/03/05/business/media/msnbc-bernie-sanders-media.html) | 7 | N | N | Y | Sanders and MSNBC | Very Related |
| [Democrats, Don’t Abandon Fox News](https://www.nytimes.com/2019/03/08/opinion/fox-news-democrats-debate.html) | 7 | N | N | N | Democrats and Fox News | Very Related |
| [Candidates Running Against, and With, Cable News](https://www.nytimes.com/2010/10/24/us/politics/24cable.html) | 4 | Y | Y | Y | Fox, MSNBC and politics  | Related |

### King Of Speed

勝者を結論づける前に、パフォーマンス時間について話をする必要があります。それぞれのアルゴリズムは、速度の点で非常に異なった性能を発揮しました。

その結果、TF-IDFの実装は他のどのアルゴリズムよりもはるかに高速であった。最初から最後まで（トークン化、ベクトル化、比較）33,914文書を1つのCPUで計算するのにかかった。

- TF-IDF: 1.5min
- Jaccard: 13min
- Doc2vec: 43min
- USE: 62min
- BERT: 50+ hours(各文章はベクトル化)

TF-IDFの所要時間はわずか1分半。これはUSEでかかった時間の2.5%です。もちろん、複数の効率化を取り入れることは可能です。しかし、潜在的な利得を最初に議論する必要があります。それは、開発の難易度のトレードオフを厳しく見極める別の理由を私たちに与えてくれるでしょう。

#### Here’s the winner algorithms from each article.
1. BERT
2. TF-IDF
3. TF-IDF
4. Jaccard, TF-IDF, USEで同位
5. USE


この結果から、ニュース記事でのドキュメントの類似性を考えると、TF-IDFが最有力候補だと言えます。これは、最小限のカスタマイズで使用する場合に特に当てはまります。また、TF-IDFが発明されてから2番目に古いアルゴリズムであることを考えると、これは驚くべきことです。むしろ、現代の最先端のAIディープラーニングがこのタスクでは何の意味もないことにがっかりするかもしれません。

もちろん、それぞれの深層学習技術は、自分のモデルを訓練し、データをより良く前処理することで改善することができます。しかし、すべての手法には開発コストがかかります。その努力がナイーブTF-IDF法と比較してどれだけ良い結果をもたらすのか、よく考えてみる必要があります。

最後に、文書の類似性において、Jaccard と Doc2vog を完全に忘れるべきだと言ってもいいでしょう。これらは今日の代替手段と比較して何のメリットもありません。


### Recommendation For Starters
あなたのアプリケーションにゼロから類似性アルゴリズムを実装することを決めたとしましょう。

#### 1. Implement TF-IDF first
ディープラーニングの誇大広告にもかかわらず、文書の類似性照合における最先端の技術はTF-IDFです。高品質の結果が得られます。そして何よりも高速です。

これまで見てきたように、ディープラーニング手法にアップグレードすることで、より良いパフォーマンスが得られるかもしれませんし、得られないかもしれません。多くの思考は、トレードオフを計算するために事前に配置する必要があります。

#### 2. Accumulate Better Data
アンドリュー・ンは2017年に「データは新しいオイル」という類推をしました。オイルなしで車が動くとは思えない。そして、そのオイルは良いものでなければならない。

ドキュメントの類似性は、特定のアルゴリズムと同じくらいデータの多様性に依存している。類似性の結果を向上させるために、ユニークなデータを見つけることに最も力を注ぐべきです。

#### 3. Upgrade to Deep Learning
TF-IDFの結果に不満がある場合のみ、USEまたはBERTに移行する。データパイプラインを設定し、インフラをアップグレードします。爆発的な計算時間を考慮する必要があります。おそらく、単語の埋め込みを前処理することになるだろうから、類似性マッチングを実行時間ではるかに速く処理できるようになる。Googleがこのトピックの[チュートリアル](https://cloud.google.com/solutions/machine-learning/building-real-time-embeddings-similarity-matching-system)を書いています。

#### 4. Tweak the Deep Learning Algorithm
ゆっくりと自分のモデルをアップグレードしていくことができます。自前のモデルを訓練したり、事前に訓練したものを特定の領域に当てはめたりなど また、今日では多くの異なる深層学習モデルが利用可能です。どれがあなたの特定の要件に最もフィットするかを確認するために、1つずつ試してみることができます。

### Document Similarity Is One Of Many NLP Tasks

様々なアルゴリズムで文書の類似性を達成することができます：あるものは伝統的な統計的アプローチであり、他のものは最先端のディープラーニング手法です。実際のニューヨークタイムズの記事で、それらがどのように比較されているかを見てきました。

TF-IDFを使えば、ローカルのラップトップで簡単に文書の類似性の検証を始めることができます。派手なGPUは必要ありません。大容量のメモリも必要ありません。高品質のデータを使用しても、競争力のある結果を得ることができます。

センチメント分析や分類などの他のタスクをしたい場合は、深層学習があなたの仕事に適しているはずです。しかし、研究者たちはディープラーニングの効率と性能の境界線を押し広げようとしているが、誇大広告のループの中で生活することは、私たち全員にとって健康的ではない。それは新参者にとってとてつもない不安と不安を生む。

経験的であり続けることで、現実から目を離さないことができます。

うまくいけば、このブログがあなた自身のNLPプロジェクトを始めるための励みになっていることを願っています。

さあ、手を汚して始めましょう。


### Further Reading
- An article covering TF-IDF and Cosine similarity with examples: “[Overview of Text Similarity Metrics in Python](https://towardsdatascience.com/overview-of-text-similarity-metrics-3397c4601f50)”.
- An academic paper discussing how cosine similarity is used in various NLP machine learning tasks: “[Cosine Similarity](https://www.sciencedirect.com/topics/computer-science/cosine-similarity)”.
- Discussion of sentence similarity in different algorithms: “[Text Similarities : Estimate the degree of similarity between two texts](https://medium.com/@adriensieg/text-similarities-da019229c894)”.
- An examination of various deep learning models in text analysis: “[When Not to Choose the Best NLP Model](https://blog.floydhub.com/when-the-best-nlp-model-is-not-the-best-choice/)”.
- Conceptual dive into BERT model: “[A review of BERT based models](https://towardsdatascience.com/a-review-of-bert-based-models-4ffdc0f15d58)”.
- A literature review on document embeddings: “[Document Embedding Techniques](https://towardsdatascience.com/document-embedding-techniques-fed3e7a6a25d)”


記事著者の方が参画しているプロジェクトKaffeのリンク -> https://kaffae.com/

Chrome ウェブストア -> https://chrome.google.com/webstore/detail/read-with-kaffae/cdopdmmkjbdmffleiaajlplpgfbikekc

ウェブストアの概要説明
```
読んだことを忘れない。マインドフルな読書を簡単に。
あなたが読んだものをもっと覚えよう。マインドフル・リーディングを簡単に。

Kaffae extensionを使えば、毎日の読書の仕方を簡単に意識することができます。あなたの読書をバックグラウンドで自動的に追跡・分析します。

ニューヨークタイムズ、BBC、ミディアム、ニューヨーカー、ウィキペディアなどの出版社の本を読む時間が長い人に最適です。

日刊レポート ★デイリーレポート

毎朝、ノートパソコンを開くと、毎日のように読書の様子が更新されます。私たちは読んだものの80％を、再び露出がない限り忘れてしまいます。この間隔をあけて繰り返すことが、情報を保持するための効果的な方法です。
```
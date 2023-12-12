# Changelog

## [0.3.3](https://github.com/leoisl/plasnet/compare/v0.3.2...v0.3.3) (2023-12-12)


### Continuous Integration

* just running coverage if python version is 3.11 ([2084763](https://github.com/leoisl/plasnet/commit/20847632d7016baf3e4448c5e41c5c576b725e43))


### Bug Fixes

* fix a bug where plasnet was not correctly recognising blackholes in type command ([92bbefa](https://github.com/leoisl/plasnet/commit/92bbefac76458345bf4e5830ed2adf00a1e4c623))

## [0.3.2](https://github.com/leoisl/plasnet/compare/v0.3.1...v0.3.2) (2023-11-27)


### Bug Fixes

* now setting the default colour for blackhole plasmids instead of erroring out with KeyError ([fa966d2](https://github.com/leoisl/plasnet/commit/fa966d2d78412a70b9dea0e268ce83b1d2311e94))

## [0.3.1](https://github.com/leoisl/plasnet/compare/v0.3.0...v0.3.1) (2023-11-17)


### Continuous Integration

* re-enabling python versions 3.8, 3.9 and 3.10 in the CI tests ([c30c2a0](https://github.com/leoisl/plasnet/commit/c30c2a03a1f9586380976023d1796082b3d71a9b))


### Documentation

* small fix to the link of add-sample-hits output in README.md ([ef945bf](https://github.com/leoisl/plasnet/commit/ef945bf6cb48d20c44d984e2b5e9acd0c3089305))

## [0.3.0](https://github.com/leoisl/plasnet/compare/v0.2.0...v0.3.0) (2023-11-17)


### Documentation

* updating README.md with add-sample-hits subcommand documentation ([2df8bc5](https://github.com/leoisl/plasnet/commit/2df8bc5246cdd99c24505ee4ff523cd2adca3868))


### Features

* adding ListOfSampleGraphs class ([0b29530](https://github.com/leoisl/plasnet/commit/0b2953005045cceea9f59e0db43d203bcfc72449))
* adding SampleGraph class ([e673f36](https://github.com/leoisl/plasnet/commit/e673f361ed71ebef443f569c394599bb07550d67))
* adding subcommand add-sample-hits ([34c25b9](https://github.com/leoisl/plasnet/commit/34c25b9a12439a01afa7dd9ed2654af237331519))


### Bug Fixes

* adding SampleGraph.from_subcommunity_graph() ([398d863](https://github.com/leoisl/plasnet/commit/398d863a1f6a32c3f26d80d80105b39a0ea1bf23))
* fixing BaseGraph.get_induced_components() ([d9e277c](https://github.com/leoisl/plasnet/commit/d9e277c2bc6ae3bc8e27f609be7919806b39cb22))
* fixing HTML sample filters production ([8db01bc](https://github.com/leoisl/plasnet/commit/8db01bc08ab7c740c8bac089aca2bbf8e76f955e))
* fixing OutputProducer.produce_subcommunities_visualisation() typing ([90875c4](https://github.com/leoisl/plasnet/commit/90875c446d655e25fabd4d5ebd406cedfe8591c6))
* fixing SampleGraph constructor ([f5edfb0](https://github.com/leoisl/plasnet/commit/f5edfb09f21dc06c4f1dba991af1bb403ba90b32))
* removing unused tag in index_template.html ([33d9690](https://github.com/leoisl/plasnet/commit/33d96901b7a41073429c1901e7e8c62d04c2b193))


### Code Refactoring

* adding attribute description to BaseGraph instead of computing it when producing visualiation ([a2496fc](https://github.com/leoisl/plasnet/commit/a2496fcd0ef9cc50e575c190edc2a2bb5d27e084))
* adding attribute path to BaseGraph instead of computing it when producing the visualisation ([4367bc0](https://github.com/leoisl/plasnet/commit/4367bc03bb8ff8a85e89ed8e58e92ea1c89f323f))
* adding method ListOfGraphs.get_graphs_sorted_by_size() instead of computing this during visualisation ([69d1db7](https://github.com/leoisl/plasnet/commit/69d1db756ed99beea1e018a3e64f7554a09655ce))
* big refactor in OutputProducer, using the previous changes to produce visualisation ([750a8de](https://github.com/leoisl/plasnet/commit/750a8decc9f87c31556d2576b1ff376dfda9146b))
* graph parameter in BaseGraph classes and its subclasses is now properly typed as Optional ([09f92cf](https://github.com/leoisl/plasnet/commit/09f92cf41cd615342c1ebd2dd34b098bc7c2829e))
* ListOfSampleGraphs -&gt; SampleGraphs ([9062ca2](https://github.com/leoisl/plasnet/commit/9062ca266b1d927dfadb01a6d14ac8b3d8682c30))
* removing old code to add sample hits from BaseGraph ([4445907](https://github.com/leoisl/plasnet/commit/444590762fe248dd04a4130c63de0de4423b1737))


### Tests

* adding add-sample-hits integration test ([f700e88](https://github.com/leoisl/plasnet/commit/f700e88f603ea9329e64ff758244a637827ad56f))
* adding subcommunities pickle to test data ([d216dcc](https://github.com/leoisl/plasnet/commit/d216dcc6acf226cc072afb6493b7ee98ad274c8d))
* updating test data ([6e33af4](https://github.com/leoisl/plasnet/commit/6e33af45d6c05b6a855c01861bc1313d38d6eb5c))

## [0.2.0](https://github.com/leoisl/plasnet/compare/v0.1.7...v0.2.0) (2023-11-14)


### Continuous Integration

* removing conventional-prs.yaml ([ef78901](https://github.com/leoisl/plasnet/commit/ef78901d0c91a6cf585c6c1811fbb27be35446b7))
* temporarily removing pylint from pre-commit and ci ([d821f19](https://github.com/leoisl/plasnet/commit/d821f1949e6b677acff6090a8a9b6b71408e7793))


### Features

* edges now show the split and type distance in their labels ([51c5c00](https://github.com/leoisl/plasnet/commit/51c5c00d42544f80baf1b3b7277353fac0d36db2))


### Bug Fixes

* colouring the original communities, pre-typing, in the type command ([0fc3821](https://github.com/leoisl/plasnet/commit/0fc382151c42959a126ef91b8e3f531107096edc))
* removing redundant attribute BlackholeGraph._original_graph ([4e622e0](https://github.com/leoisl/plasnet/commit/4e622e0d074a0e0b87360fe0d1f9f098e72a4149))


### Tests

* updating tests/data/communities.pkl ([11c4588](https://github.com/leoisl/plasnet/commit/11c4588b211ccec4fa2ddb814f3cade2e3fdc000))

## [0.1.7](https://github.com/leoisl/plasnet/compare/v0.1.6...v0.1.7) (2023-11-14)


### Continuous Integration

* now correctly making release-pypi deploy to pypi once a release is published ([f05f764](https://github.com/leoisl/plasnet/commit/f05f7644595312da106facb210709ed4d5c91a48))

## [0.1.6](https://github.com/leoisl/plasnet/compare/v0.1.5...v0.1.6) (2023-11-13)


### Continuous Integration

* allowing release-pypi workflow to be manually triggered ([38b8edc](https://github.com/leoisl/plasnet/commit/38b8edce2ad0cb106722fe895c91f164b482023d))

## [0.1.5](https://github.com/leoisl/plasnet/compare/v0.1.4...v0.1.5) (2023-11-13)


### Continuous Integration

* running release-pypi when release is published ([442bdb6](https://github.com/leoisl/plasnet/commit/442bdb6a327a34c910b578e71037d91945fdd46a))

## [0.1.4](https://github.com/leoisl/plasnet/compare/v0.1.3...v0.1.4) (2023-11-13)


### Continuous Integration

* release-pypi now triggered when a release is created ([8bcb724](https://github.com/leoisl/plasnet/commit/8bcb724f28ced3a671a76146510bb3cd38813f65))

## [0.1.3](https://github.com/leoisl/plasnet/compare/v0.1.2...v0.1.3) (2023-11-13)


### Continuous Integration

* automatically uploading plasnet results to gh-pages ([97a434e](https://github.com/leoisl/plasnet/commit/97a434ea15f846f3d4e68ad45f4690588519f537))
* just generating new visualisations with pushes to the main branch ([3babbcb](https://github.com/leoisl/plasnet/commit/3babbcb059a893cabd6b6ee60b0d7a25875a2c9d))
* setting up poetry before installing ([e345f4b](https://github.com/leoisl/plasnet/commit/e345f4bf3d41e6907dec658ae29e54eed097a7eb))


### Documentation

* adding links to the latest visualisations to README ([4af8669](https://github.com/leoisl/plasnet/commit/4af8669452f6c0734e25182aa47bfc4a90d4637a))

## [0.1.2](https://github.com/leoisl/plasnet/compare/v0.1.1...v0.1.2) (2023-11-13)


### Build System

* adding coverage to dev deps ([263646d](https://github.com/leoisl/plasnet/commit/263646d21dd020f4c3a53354af377abcf49e4932))
* adding test command to Makefile ([6b20632](https://github.com/leoisl/plasnet/commit/6b206329ea65ab9d228ae6cf0fe50df5c0f248e8))
* removing tag command from Makefile ([9a7f562](https://github.com/leoisl/plasnet/commit/9a7f5629b343fc763dcfce8426ea7be595706322))
* updating make coverage ([eecb53f](https://github.com/leoisl/plasnet/commit/eecb53ff76671fb5a121c063986210be80aed902))


### Continuous Integration

* adding coverage badge ([584b9cc](https://github.com/leoisl/plasnet/commit/584b9cc53c7b50cd45a0c90a1239a8d82bca908d))
* CI debugging ([72c1b53](https://github.com/leoisl/plasnet/commit/72c1b539d97d5935515ec38d279ce9fee56b0089))
* CI debugging ([64d083c](https://github.com/leoisl/plasnet/commit/64d083c2169adbc8268481fe819ccc59d82fd3cc))
* now running make coverage ([fd0d2c1](https://github.com/leoisl/plasnet/commit/fd0d2c1b6d3845fb3836d454263e8355a0e8fde5))
* now running tests in CI ([95bc22a](https://github.com/leoisl/plasnet/commit/95bc22a5a3317af2ee4e064b52747cd385fc643a))
* trying to fix Coverage Push changes step in CI ([44a77cb](https://github.com/leoisl/plasnet/commit/44a77cbd4042a4794ea6ac9b714693f674816b02))


### Miscellaneous Chores

* updating readme with badges ([aa4e700](https://github.com/leoisl/plasnet/commit/aa4e7001de139adf9f4ac1c2fc3a545f5756a802))


### Documentation

* updating README installation and usage ([29acd34](https://github.com/leoisl/plasnet/commit/29acd34618f94149066002fe27f408cf7932ac9f))


### Tests

* adding integration test data ([e718a7b](https://github.com/leoisl/plasnet/commit/e718a7bb3d938d9a4c1ad83ee2faafe086df1bc4))
* adding split and type command integration tests ([191c049](https://github.com/leoisl/plasnet/commit/191c04923e4c2cb6fdc04a11d87fb86af8d7c4ce))

## [0.1.1](https://github.com/leoisl/plasnet/compare/v0.1.0...v0.1.1) (2023-11-13)


### Continuous Integration

* adding release-pypi workflow for tagged commits ([4b9df0e](https://github.com/leoisl/plasnet/commit/4b9df0e3d7fb9ba42ac28d575988fe5f59af6ba0))

## 0.1.0 (2023-11-13)


### Build System

* adding mypy to dev deps ([5cac9e6](https://github.com/leoisl/plasnet/commit/5cac9e6e583108ffb9cf3dfa9da0fa492fb3c61d))


### Continuous Integration

* adding convetional-prs action ([75015ff](https://github.com/leoisl/plasnet/commit/75015ff594452b606ff729941b31cfebebd66e3e))
* adding release-please action ([0cb02c8](https://github.com/leoisl/plasnet/commit/0cb02c8ad06e4d1ac83fb7f5733fa90835e0c97a))
* improving CI script and installing plasnet ([8377b7d](https://github.com/leoisl/plasnet/commit/8377b7d836c844593395f33bb66ab365bc58401f))
* temporarily using python version 3.11 to save resources ([cd99d2f](https://github.com/leoisl/plasnet/commit/cd99d2f785c86cd3dfb6b1f71cc03e3a521de8bc))
* testing ci fail ([3c32e95](https://github.com/leoisl/plasnet/commit/3c32e9558aaf90af82edd27b7dfc538bd7f80146))
* using the correct default branch ([790fd34](https://github.com/leoisl/plasnet/commit/790fd346e95e08d76cb96e9bc966d92d7150c6b7))


### Miscellaneous Chores

* adding Makefile ([b9381ce](https://github.com/leoisl/plasnet/commit/b9381ce224f5f03384a83d616ac468e6970a8cc9))
* adding pylint to dev-deps ([45931e5](https://github.com/leoisl/plasnet/commit/45931e5e34f0349dc493e2de4d3bdbc613492e85))
* pre-commit now failing fast and adding commented out pylint hook ([dd64f2a](https://github.com/leoisl/plasnet/commit/dd64f2a9545cdebc2a8f31a3e4ca6eba814d9ea1))
* pylint now runs but pre-commit does not fail if it fails ([e00ee75](https://github.com/leoisl/plasnet/commit/e00ee751f44e58c9d4be8b6cae407fcde2300cc5))


### Features

* adding colours to subcommunities visualisation ([730bcc5](https://github.com/leoisl/plasnet/commit/730bcc56459d8da91e5d207de6c3f280d603c67d))
* adding commitlint to the repo ([b719203](https://github.com/leoisl/plasnet/commit/b719203fe5181308bfafc90601f31e022342a213))
* adding conventional commit checking through pre-commit ([273d9df](https://github.com/leoisl/plasnet/commit/273d9df444bcfc4ad19ce831991e37213bcb7b4d))
* adding flake8, black and isort to dev deps ([a192108](https://github.com/leoisl/plasnet/commit/a1921088c41ade4e75fc6deb1fb19131ce8f9c75))
* adding initial Makefile with pre_commit rule ([2b9b32d](https://github.com/leoisl/plasnet/commit/2b9b32daf60736a8f9892325fb6fb11f21482c4e))
* adding remove_plasmids() to BaseGraph ([be7e729](https://github.com/leoisl/plasnet/commit/be7e729dc30ab67aa0920e05adc7d35a23f5f54f))
* adding seed-isort-config to auto config known_third_party ([42d8879](https://github.com/leoisl/plasnet/commit/42d88790dd80ef62d85ee11dabc9140ce879890b))
* now adding subcommunity colours to the community vis. in the type subcommand ([9f7fe62](https://github.com/leoisl/plasnet/commit/9f7fe62f842cacceba7a9af50e89ad30842a56fe))
* now creating objects/communities.tsv file describing the community clustering in the split subcommand ([511d677](https://github.com/leoisl/plasnet/commit/511d677293a1d9895fa56a066e2d685f25b619a7))
* outputting an objects/typing.tsv file describing the typing for the type subcommand ([690fc84](https://github.com/leoisl/plasnet/commit/690fc849c28838145633098f455ecf6b7eb60513))
* outputting binary objects in the type subcommand ([49f0c4c](https://github.com/leoisl/plasnet/commit/49f0c4cbb28da27d94e7775be8d876bd0d0086c2))
* running pre-commit during CI ([3c930e5](https://github.com/leoisl/plasnet/commit/3c930e5cdc384ae5d4a4ea18d7a20d98276c6176))


### Bug Fixes

* adding --version to the CLI ([7c8aee9](https://github.com/leoisl/plasnet/commit/7c8aee93378dc3ef15eb4b1d8a5cadc6506a4ce4))
* adding more logging to the type subcommand ([9168ff9](https://github.com/leoisl/plasnet/commit/9168ff9d039c21df59625479709a6a12a03e8056))
* adding the main import back to plasnet/__init__.py ([1b87f48](https://github.com/leoisl/plasnet/commit/1b87f48d1eeb50b0de1ce9c38d82414e3a5a693b))
* addint stubs to mypy and making it strict ([dbba7b3](https://github.com/leoisl/plasnet/commit/dbba7b339e07db0b0326567c5cda3df387a68a84))
* all_subcommunities in the type subcommand is now Subcommunities instead of list[Subcommunities] ([ff00cde](https://github.com/leoisl/plasnet/commit/ff00cde3f9024dab151fdfbaf2af51326cab1405))
* BaseGraph.get_induced_components() now actually retruning a BaseGraph ([a3e390f](https://github.com/leoisl/plasnet/commit/a3e390f2165fb3ae2df7614df7dc50d0a43bf303))
* casting Communities to itself ([9719792](https://github.com/leoisl/plasnet/commit/97197920c67ae800f5b699b62802b4cfa157bd6a))
* doing pre-commit linting/formatting properly now ([a9f16e4](https://github.com/leoisl/plasnet/commit/a9f16e4b9232ba3caea6c82da870520ee1de4c27))
* explicitly exporting attribute 'main' in plasnet package ([d8f00d8](https://github.com/leoisl/plasnet/commit/d8f00d8f0674ba73a9de8fbe2b5f1dbe735d8d55))
* fixing BaseGraph and ListOfGraphs typings ([8e41e76](https://github.com/leoisl/plasnet/commit/8e41e7663fa7d9e6050477b17ff85b0924fe8c36))
* fixing BaseGraph constructor and all the hierarchy constructors and adding the label attribute ([a3e7916](https://github.com/leoisl/plasnet/commit/a3e79165a6712e2a1a1d2c4703618356205644fa))
* fixing implementation of CommunityGraph.split_graph_into_subcommunities ([6fdacc7](https://github.com/leoisl/plasnet/commit/6fdacc7b1c1d1d2bb199ea9f6e7d59229d80dffa))
* fixing implementation of OutputProducer.produce_subcommunities_visualisation() ([6e455f8](https://github.com/leoisl/plasnet/commit/6e455f81c48ad5ff494ba507b900d4c35db3cd41))
* fixing small import issue in community_graph.py ([83474cd](https://github.com/leoisl/plasnet/commit/83474cd4ae12d7643b6da266c297fae7350e96f5))
* fixing type subcommand description ([7ef7dcf](https://github.com/leoisl/plasnet/commit/7ef7dcfe17a6b9312baee9aeb4096b3eb15fe09b))
* fixing type subcommand implementation ([b99a412](https://github.com/leoisl/plasnet/commit/b99a4122e0afba876c81d6be8b28951214f41314))
* improving linting ([bb7fd3a](https://github.com/leoisl/plasnet/commit/bb7fd3a79dcbbac5742eef47a67634bdc0ff0c9e))
* improving pre-commit config ([b066a0f](https://github.com/leoisl/plasnet/commit/b066a0ffff6316e6953695a38614dbb8890cbb1a))
* improving Subcommunities inheritance ([345c31f](https://github.com/leoisl/plasnet/commit/345c31fba2e4796fbfefbbee53efa1a77a8abaa8))
* Improving SubcommunityGraph inheritance and implementing required methods ([45e18b4](https://github.com/leoisl/plasnet/commit/45e18b445f200dfde2d18dc70025ea7f1074cd02))
* managing pre-commit configs through .pre-commit-config.yaml ([27587a7](https://github.com/leoisl/plasnet/commit/27587a78efa61a865926846e2df4c84e6b1cd2ae))
* now keeping mypy and flake8 logs when pre-committing ([7f00712](https://github.com/leoisl/plasnet/commit/7f00712f45e892fe2e5a6cb2320dd0233837ded7))
* now outputting subcommunities and refactoring communities outputting ([b5b7d68](https://github.com/leoisl/plasnet/commit/b5b7d689fba4dad4bec42b5f6cc8f6b9eee4ba3b))
* PlasmidGraph.build() now actually returning a PlasmidGraph ([a739a58](https://github.com/leoisl/plasnet/commit/a739a580773516ca99c674c048971ec97efd7026))
* plasnet.main() does not return anything ([206ea6a](https://github.com/leoisl/plasnet/commit/206ea6ae4fdbd72302cc244971fd54059ccc0f25))
* reducing max line length from 120 to 100 ([72d8f76](https://github.com/leoisl/plasnet/commit/72d8f769b2b8cd1af385e3483902bcb3c8ebebf6))
* removing husky and commitlint config - all done through pre-commit now ([061b5b8](https://github.com/leoisl/plasnet/commit/061b5b89592a889b53f33370dd0a858f61db6265))
* removing redundant noqa ([0ccb383](https://github.com/leoisl/plasnet/commit/0ccb3836b88c813231d10653534bd320946218b2))
* removing verbosity from pre-commits ([a82c582](https://github.com/leoisl/plasnet/commit/a82c582b8050d586953639aacc0ff5298880e3b0))
* updating pre-commit deps ([acae5f6](https://github.com/leoisl/plasnet/commit/acae5f6fc76a68ccb54c82c1d5f23f8279720672))
* updating readme ([081610d](https://github.com/leoisl/plasnet/commit/081610d2bf16e4af5950a81acc8e4e5db2e3a677))
* using the graph label for filename and label instead of generating them on the fly ([6a98166](https://github.com/leoisl/plasnet/commit/6a98166fb067454fb9fc45f3bc9ab2d5fda12399))


### Code Refactoring

* adding a comment to Makefile ([7fad449](https://github.com/leoisl/plasnet/commit/7fad44990286b044fe98ffb2ea1291445661590d))
* adding an important comment to .pre-commit-config.yaml ([5db6074](https://github.com/leoisl/plasnet/commit/5db6074335e0f65d0a3229525e24e123d35a65f8))
* black ([a4d8aa2](https://github.com/leoisl/plasnet/commit/a4d8aa2f4c2e421e9fa83d60c11db825b6391c22))
* black reformatting ([a470b9f](https://github.com/leoisl/plasnet/commit/a470b9fa540e1c76463d34c5f7e46b6e938d8803))
* extracting class BlackholeGraph from CommunityGraph ([0706794](https://github.com/leoisl/plasnet/commit/0706794d3c5fdcc78f39483c8cf5e01579a9cd9d))
* flake8 ([0178225](https://github.com/leoisl/plasnet/commit/01782256e8ffe36db6725bbf9aa6d0158079b4ad))
* improving overall typing ([59ff4e0](https://github.com/leoisl/plasnet/commit/59ff4e0a6d234a671093396f0908be2aaf43f6e3))
* isort ([8a1a0c6](https://github.com/leoisl/plasnet/commit/8a1a0c606d7064e69d086e192d0b0a0c81ded72c))
* linting ([87cb9f2](https://github.com/leoisl/plasnet/commit/87cb9f25ada0017dfd87f6447aa7e250492ebcf2))
* OutputProducer.produce_subcommunities_visualisation() now receives Subcommunities instead of list[Subcommunities] ([0bfd9e7](https://github.com/leoisl/plasnet/commit/0bfd9e79055737aff2aa2d00fdbc8cbbef66e26f))
* removing unused import pickle ([5206a38](https://github.com/leoisl/plasnet/commit/5206a38a1e60e23f8e98e9fbb0c08bacd21e5ac0))
* small typing refactor: List -&gt; list ([32d240b](https://github.com/leoisl/plasnet/commit/32d240bb9b63929c6d3f3a66422a91bf176f9444))
* type of our nodes is str ([d7fac0b](https://github.com/leoisl/plasnet/commit/d7fac0bd5b53c7430baa78e83a64156a68678ca6))
* **typing:** improving ListOfGraphs.load() typing ([68b60ae](https://github.com/leoisl/plasnet/commit/68b60aec5ab39289a7c49a25468be74d834b27da))
* unused methods cleanup ([223fc13](https://github.com/leoisl/plasnet/commit/223fc134385a06f3497283506f9cb4c73100ba36))

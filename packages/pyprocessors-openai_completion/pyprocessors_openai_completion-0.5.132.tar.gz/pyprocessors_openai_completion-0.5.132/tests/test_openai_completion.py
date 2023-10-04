import json
import os
from pathlib import Path

import pytest
import requests
from dirty_equals import HasLen, HasAttributes, IsList, IsPartialDict
from pymultirole_plugins.v1.schema import Document, DocumentList, Sentence

from pyprocessors_openai_completion.openai_completion import (
    OpenAICompletionProcessor,
    OpenAICompletionParameters,
    OpenAIModel,
    flatten_document, OpenAIFunction, AzureOpenAICompletionProcessor,
    DeepInfraOpenAICompletionProcessor, AzureOpenAICompletionParameters,
    AZURE_CHAT_GPT_MODEL_ENUM, CHAT_GPT_MODEL_ENUM, DeepInfraOpenAICompletionParameters
)


def test_openai_completion_basic():
    model = OpenAICompletionProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == OpenAICompletionParameters

    model = AzureOpenAICompletionProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == AzureOpenAICompletionParameters

    model = DeepInfraOpenAICompletionProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == DeepInfraOpenAICompletionParameters


def test_flatten_doc():
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/complexdoc.json",
    )
    with source.open("r") as fin:
        jdoc = json.load(fin)
        doc = Document(**jdoc)
        flatten = flatten_document(doc)
        assert flatten == IsPartialDict(
            text=doc.text,
            title=doc.title,
            metadata_foo=doc.metadata["foo"],
            altTexts_0_name=doc.altTexts[0].name,
        )


JINJA_PROMPTS = {
    "preserve_entities": """Generates several variants of the following context while preserving the given named entities. Each named entity must be between square brackets using the notation [label:entity].
    Context: {{ doc.text }}
    {%- set entities=[] -%}
    {%- for a in doc.annotations -%}
      {%- do entities.append('[' + a.label + ':' + a.text + ']') -%}
    {%- endfor %}
    Given named entities using the notation [label:entity]: {{ entities|join(', ') }}
    Output language: {{ doc.metadata['language'] }}
    Output format: bullet list""",
    "substitute_entities": """Generates several variants of the following context while substituting the given named entities by semantically similar named entities with the same label, for each variant insert the new named entities between square brackets using the notation [label:entity].
    Context: {{ doc.text }}
    {%- set entities=[] -%}
    {%- for a in doc.annotations -%}
      {%- do entities.append('[' + a.label + ':' + a.text + ']') -%}
    {%- endfor %}
    Given named entities using the notation [label:entity]: {{ entities|join(', ') }}
    Output language: {{ doc.metadata['language'] }}
    Output format: bullet list""",
}


# @pytest.mark.skip(reason="Not a test")
@pytest.mark.skip(reason="Not a test")
@pytest.mark.parametrize("typed_prompt", [p for p in JINJA_PROMPTS.items()])
def test_jinja_doc(typed_prompt):
    type = typed_prompt[0]
    prompt = typed_prompt[1]
    parameters = OpenAICompletionParameters(
        max_tokens=3000,
        completion_altText=type,
        prompt=prompt,
    )
    processor = OpenAICompletionProcessor()
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/jinjadocs.json",
    )
    with source.open("r") as fin:
        jdocs = json.load(fin)
        docs = [Document(**jdoc) for jdoc in jdocs]
        docs = processor.process(docs, parameters)
        assert docs == HasLen(6)
        sum_file = testdir / f"data/jinjadocs_{type}.json"
        dl = DocumentList(__root__=docs)
        with sum_file.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
    # noqa: E501


def chunks(seq, size=1000):  # noqa
    return (seq[pos: pos + size] for pos in range(0, len(seq), size))


@pytest.mark.skip(reason="Not a test")
def test_semeval_docs():
    start_at = 32
    parameters = OpenAICompletionParameters(
        max_tokens=3000,
    )
    processor = OpenAICompletionProcessor()
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/semeval_fa_da.json",
    )
    with source.open("r") as fin:
        jdocs = json.load(fin)
        for i, chunk in enumerate(chunks(jdocs, 10)):
            if i >= start_at:
                docs = [Document(**jdoc) for jdoc in chunk]
                for type, prompt in JINJA_PROMPTS.items():
                    parameters.prompt = prompt
                    parameters.completion_altText = type
                    docs = processor.process(docs, parameters)
                    # assert docs == HasLen(6)
                    sum_file = testdir / f"data/semeval_fa_da_{type}_{i}.json"
                    dl = DocumentList(__root__=docs)
                    with sum_file.open("w") as fout:
                        print(
                            dl.json(exclude_none=True, exclude_unset=True, indent=2),
                            file=fout,
                        )


@pytest.mark.skip(reason="Not a test")
@pytest.mark.parametrize("model", [m for m in CHAT_GPT_MODEL_ENUM])
def test_openai_prompt(model):
    parameters = OpenAICompletionParameters(
        model=model, max_tokens=120, completion_altText="completion"
    )
    processor = OpenAICompletionProcessor()
    docs_with_prompts = [
        (
            Document(
                identifier="1",
                text="séisme de magnitude 7,8 a frappé la Turquie",
                metadata={"language": "fr"},
            ),
            "Peux tu écrire un article de presse concernant: $text",
        ),
        (
            Document(
                identifier="2",
                text="j'habite dans une maison",
                metadata={"language": "fr"},
            ),
            "Peux tu me donner des phrases similaires à: $text",
        ),
        (
            Document(
                identifier="3",
                text="il est né le 21 janvier 2000",
                metadata={"language": "fr"},
            ),
            "Peux tu me donner des phrases similaires en changeant le format de date à: $text",
        ),
        (
            Document(
                identifier="4",
                text="""Un nuage de fumée juste après l’explosion, le 1er juin 2019.
                Une déflagration dans une importante usine d’explosifs du centre de la Russie a fait au moins 79 blessés samedi 1er juin.
                L’explosion a eu lieu dans l’usine Kristall à Dzerzhinsk, une ville située à environ 400 kilomètres à l’est de Moscou, dans la région de Nijni-Novgorod.
                « Il y a eu une explosion technique dans l’un des ateliers, suivie d’un incendie qui s’est propagé sur une centaine de mètres carrés », a expliqué un porte-parole des services d’urgence.
                Des images circulant sur les réseaux sociaux montraient un énorme nuage de fumée après l’explosion.
                Cinq bâtiments de l’usine et près de 180 bâtiments résidentiels ont été endommagés par l’explosion, selon les autorités municipales. Une enquête pour de potentielles violations des normes de sécurité a été ouverte.
                Fragments de shrapnel Les blessés ont été soignés après avoir été atteints par des fragments issus de l’explosion, a précisé une porte-parole des autorités sanitaires citée par Interfax.
                « Nous parlons de blessures par shrapnel d’une gravité moyenne et modérée », a-t-elle précisé.
                Selon des représentants de Kristall, cinq personnes travaillaient dans la zone où s’est produite l’explosion. Elles ont pu être évacuées en sécurité.
                Les pompiers locaux ont rapporté n’avoir aucune information sur des personnes qui se trouveraient encore dans l’usine.
                """,
                metadata={"language": "fr"},
            ),
            "Peux résumer dans un style journalistique le texte suivant: $text",
        ),
        (
            Document(
                identifier="5",
                text="Paris is the capital of France and Emmanuel Macron is the president of the French Republic.",
                metadata={"language": "en"},
            ),
            "Can you find the names of people, organizations and locations in the following text:\n\n $text",
        ),
    ]
    docs = []
    for doc, prompt in docs_with_prompts:
        parameters.prompt = prompt
        doc0 = processor.process([doc], parameters)[0]
        docs.append(doc0)
        assert doc0.altTexts == IsList(
            HasAttributes(name=parameters.completion_altText)
        )
    testdir = Path(__file__).parent / "data"
    sum_file = testdir / f"en_{model.value}.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


# noqa: E501
@pytest.mark.skip(reason="Not a test")
@pytest.mark.parametrize("model", [m for m in CHAT_GPT_MODEL_ENUM])
def test_openai_text(model):
    parameters = OpenAICompletionParameters(
        model=model,
        max_tokens=120,
        best_of=3,
        n=3,
        completion_altText="completion",
    )
    processor = OpenAICompletionProcessor()
    docs = [
        Document(
            identifier="1",
            text="Peux tu écrire un article de presse concernant: séisme de magnitude 7,8 a frappé la Turquie",
            metadata={"language": "fr"},
        ),
        Document(
            identifier="2",
            text="Peux tu me donner des phrases similaires à: j'habite dans une maison",
            metadata={"language": "fr"},
        ),
    ]
    docs = processor.process(docs, parameters)
    assert docs == HasLen(2)
    for doc in docs:
        assert doc.altTexts == IsList(HasAttributes(name=parameters.completion_altText))
    testdir = Path(__file__).parent / "data"
    sum_file = testdir / f"fr_{model.value}.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


# noqa: E501
@pytest.mark.skip(reason="Not a test")
def test_q_and_a():
    prompt = """Répondre à la question en utilisant les segments suivants et en citant les références.
    Question: {{ doc.altTexts[0].text }}
    Segments: {{ doc.text }}"""

    parameters = OpenAICompletionParameters(
        max_tokens=2000,
        completion_altText=None,
        prompt=prompt,
    )
    processor = OpenAICompletionProcessor()
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/question_segments.json",
    )
    with source.open("r") as fin:
        jdoc = json.load(fin)
        docs = [Document(**jdoc)]
        docs = processor.process(docs, parameters)
        assert docs == HasLen(1)
        sum_file = testdir / "data/question_segments_answer.json"
        dl = DocumentList(__root__=docs)
        with sum_file.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
    # noqa: E501


@pytest.mark.skip(reason="Not a test")
def test_azure_endpoint():
    parameters = AzureOpenAICompletionParameters(
        model=AZURE_CHAT_GPT_MODEL_ENUM("gpt-4"),
        max_tokens=1000,
        best_of=3,
        n=3,
        completion_altText="completion",
    )
    processor = AzureOpenAICompletionProcessor()
    docs = [
        Document(
            identifier="1",
            text="Peux tu écrire un article de presse concernant: séisme de magnitude 7,8 a frappé la Turquie",
            metadata={"language": "fr"},
        ),
        Document(
            identifier="2",
            text="Peux tu me donner des phrases similaires à: j'habite dans une maison",
            metadata={"language": "fr"},
        ),
    ]
    docs = processor.process(docs, parameters)
    assert docs == HasLen(2)
    for doc in docs:
        assert doc.altTexts == IsList(HasAttributes(name=parameters.completion_altText))
    testdir = Path(__file__).parent / "data"
    sum_file = testdir / "fr_azure_gpt_4.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        fout.write(dl.json(exclude_none=True, exclude_unset=True, indent=2))


@pytest.mark.skip(reason="Not a test")
def test_deepinfra_endpoint():
    parameters = DeepInfraOpenAICompletionParameters(
        max_tokens=100,
        completion_altText="completion",
    )
    processor = DeepInfraOpenAICompletionProcessor()
    docs = [
        Document(
            identifier="1",
            text="Peux tu écrire un article de presse concernant: séisme de magnitude 7,8 a frappé la Turquie",
            metadata={"language": "fr"},
        ),
        Document(
            identifier="2",
            text="Peux tu me donner des phrases similaires à: j'habite dans une maison",
            metadata={"language": "fr"},
        ),
    ]
    docs = processor.process(docs, parameters)
    assert docs == HasLen(2)
    for doc in docs:
        assert doc.altTexts == IsList(HasAttributes(name=parameters.completion_altText))
    testdir = Path(__file__).parent / "data"
    sum_file = testdir / "fr_llama2.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        fout.write(dl.json(exclude_none=True, exclude_unset=True, indent=2))


@pytest.mark.skip(reason="Not a test")
def test_direct_deepinfra():
    PROMPT = """[INST]Answer the question in french using the given segments of a long document and making references of those segments ["SEGMENT"] with the segment number. 
Be short and precise as possible. If you don't know the answer, just say that you don't know. Don't try to make up an answer.
Question: Est-il prévu des congés rémunérés pour les femmes souffrant de douleurs menstruelles ?

SEGMENTS:
1. À l’heure où certaines entreprises ou même certaines collectivités prévoient des congés rémunérés pour les femmes souffrant de douleurs menstruelles importantes ou d’endométriose, une proposition de loi a été déposée au Sénat en ce sens le 18 avril 2023 par une sénatrice socialiste et plusieurs de ses collègues. Les femmes concernées pourraient faire l’objet d’un arrêt de travail ou encore télétravailler, sous certaines conditions. La proposition de loi prévoit aussi un congé payé pour les femmes (et leur conjoint) ayant subi une fausse couche.

2. La proposition de loi prévoit de créer un arrêt de travail indemnisé pour les femmes souffrant de dysménorrhée (règles douloureuses) ou d’endométriose (maladie gynécologique inflammatoire et chronique). Prescrit par un médecin ou une sage-femme, cet arrêt maladie autoriserait la salariée à interrompre son travail chaque fois qu’elle se trouverait dans l’incapacité physique de travailler, pour une durée ne pouvant excéder 2 jours par mois sur une période de 3 mois. Les IJSS, versées sans délai de carence, se calculeraient selon des règles dérogatoires favorables à la salariée.  Dans l’objectif d’éviter un arrêt de travail, la proposition de loi vise aussi à favoriser la possibilité de télétravail pour les femmes souffrant de règles douloureuses et invalidantes, via l'accord collectif ou la charte sur le télétravail lorsqu'il en existe un.    Enfin, le texte propose de créer sur justification, pour les femmes affectées par une interruption spontanée de grossesse, un congé rémunéré de 5 jours ouvrables. Le conjoint, concubin ou partenaire pacsé de la salariée aurait aussi droit à ce congé.    Reste à voir si cette 2e proposition de loi, déposée le 18 avril par une sénatrice socialiste et plusieurs de ses collègues, connaîtra un sort aussi favorable que la première.

3. Maternité, paternité, adoption, femmes enceintes dispensées de travail - L’employeur doit compléter une attestation de salaire lorsque le congé de maternité* débute (c. séc. soc. art. R. 331-5, renvoyant à c. séc. soc. art. R. 323-10).      Le même document est à compléter en cas de congé d’adoption*, de congé de paternité et d’accueil de l’enfant* ou, dans le cadre de la protection de la maternité, pour les femmes travaillant de nuit ou occupant des postes à risques dispensées de travail en raison d’une impossibilité de reclassement sur un poste de jour ou sans risques .      Il s’agit de la même attestation que celle prévue pour les arrêts maladie.

4. Grossesse pathologique liée au distilbène - Le distilbène (ou diéthylstilbestrol) prescrit il y a plusieurs années entraîne des grossesses pathologiques chez les femmes qui y ont été exposées in utero.      Les femmes chez lesquelles il est reconnu que la grossesse pathologique est liée à l’exposition in utero au distilbène bénéficient d’un congé de maternité à compter du premier jour de leur arrêt de travail (loi 2004-1370 du 20 décembre 2004, art. 32         ; décret 2006-773 du 30 juin 2006, JO 2 juillet).

5. Enfant né sans vie - L'indemnité journalière de maternité est allouée même si l'enfant n'est pas né vivant au terme de 22 semaines d'aménorrhée (c. séc. soc. art. R. 331-5). Pathologie liée au Distilbène - Bien que ce médicament ne soit plus prescrit, le Distilbène (ou diéthyltilbestrol) peut entraîner des grossesses pathologiques pour les femmes qui y ont été exposées in utero. Les femmes dont il est reconnu que la grossesse pathologique est liée à l’exposition in utero au Distilbène bénéficient d’un congé de maternité à compter du premier jour de leur arrêt de travail (loi 2004-1370 du 20 décembre 2004, art. 32, JO du 21). Ces femmes peuvent prétendre à l’IJSS de maternité dès le début de leur congé de maternité si elles remplissent les conditions d’ouverture du droit au congé légal de maternité (décret 2006-773 du 30 juin 2006, JO 2 juillet).

6. Possibilité de télétravailler pour les femmes souffrant de règles douloureuses Dans l’objectif d’éviter un arrêt de travail pour douleurs menstruelles, la proposition de loi vise à favoriser la possibilité de télétravail aux femmes souffrant de dysménorrhée (proposition de loi, art. 4).   À cet égard, l'accord collectif ou la charte sur le télétravail existant dans l’entreprise devrait préciser les modalités d’accès des salariées souffrant de règles douloureuses et invalidantes à une organisation en télétravail.    En toute logique, il ressort de l’exposé des motifs que cela ne viserait que les femmes dont l’activité professionnelle est compatible avec l’exercice du télétravail.      À noter : en dehors d’un accord ou d’une charte sur le télétravail, il est toujours possible à l’employeur et au salarié de convenir d’un recours au télétravail formalisé par tout moyen (c. trav. art. L. 1222-9).Une proposition de loi en faveur des femmes souffrant de douleurs menstruelles, d’endométriose, ou ayant subi une fausse couche
    [/INST]"""
    api_key = os.getenv("DEEPINFRA_OPENAI_API_KEY")
    deploy_infer_url = "https://api.deepinfra.com/v1/inference/meta-llama/Llama-2-70b-chat-hf"
    response = requests.post(deploy_infer_url, json={
        "input": PROMPT,
        "max_new_tokens": 4096,
        "temperature": 0.2
    },
                             headers={'Content-Type': "application/json",
                                      'Authorization': f"Bearer {api_key}"})
    if response.ok:
        result = response.json()
        texts = "\n".join([r['generated_text'] for r in result['results']])
        assert len(texts) > 0


# noqa: E501

@pytest.mark.skip(reason="Not a test")
def test_function_call_ner():
    candidate_labels = {
        'per': 'Personne',
        'loc': 'Lieu géographique',
        'org': 'Organisation',
    }

    prompt = """Your task is to extract all occurences of named entities of the given labels in the provided text segments.
    Each text segment is prefixed by an index number followed by a closing parenthesis like 1) and postfixed by ===.
    Your response should include all identified named entities, their corresponding segment index numers, labels, and the start and end offsets in their correponding segment for each occurrence.
    {%- set labels=[] -%}
    {%- for l in parameters.candidate_labels.values() -%}
      {%- do labels.append('"' + l + '"') -%}
    {%- endfor %}
    Labels: {{ labels|join(', ') }}
    Segments:
    {%- for seg in doc.sentences %}
      {{ loop.index0 }}) {{ doc.text[seg.start:seg.end] }}
      ===
    {%- endfor %}"""

    parameters = OpenAICompletionParameters(
        model=OpenAIModel.gpt_3_5_turbo_16k_0613,
        max_tokens=14000,
        completion_altText=None,
        prompt=prompt,
        function=OpenAIFunction.add_annotations,
        candidate_labels=candidate_labels
    )
    processor = OpenAICompletionProcessor()
    docs = [
        Document(
            identifier="2",
            text="Cinq choses à savoir sur Toutankhamon et son fabuleux trésor\n\nL'ouverture, il y a 100 ans, du tombeau du pharaon égyptien Toutankhamon, l'une des plus grandes découvertes archéologiques de tous les temps, reste nimbée de mystères.\n\n\nVoici cinq choses à savoir sur l'enfant-roi, ses énigmes et ses trésors:\n\n\n- Un trésor inviolé -\n\n\nEn novembre 1922, après six saisons de fouilles infructueuses, l'archéologue britannique Howard Carter, son équipe égyptienne et le riche mécène Lord Carnarvon découvrent une sépulture inviolée dans la Vallée des Rois, près de Louxor en Haute-Egypte.\n\n\nLe trésor funéraire, réparti dans les cinq pièces du tombeau, est intact, avec 4.500 objets (mobilier, bijoux, statuettes), dont bon nombre en or massif.\n\n\nLe tombeau du jeune pharaon, mort à 19 ans aux environ de 1324 avant Jésus-Christ, est le seul mausolée de l'Egypte antique à avoir livré un tel trésor.\n\n\nLes innombrables autres tombeaux de pharaons et notables mis au jour jusqu'alors avaient été pillés au fil des millénaires.\n\n\n- Cercueil en or massif -\n\n\nParmi les objets découverts: un lit en bois plaqué or orné d'une tête de lion, un char ou encore un poignard au manche d'or, forgé à partir du fer de météorites selon des chercheurs.\n\n\nLe spectaculaire sarcophage en quartzite rouge hébergeait trois cercueils emboîtés les uns dans les autres, dont le dernier (110 kg) en or massif abritait la momie de Toutankhamon.\n\n\nMais la pièce maîtresse du trésor, devenue l'un des objets égyptiens les plus reconnaissables au monde, est un masque funéraire en or de plus de 10 kg incrusté de lapis-lazuli et d'autres pierres semi-précieuses.\n\n\n- Un arbre généalogique énigmatique -\n\n\nDes tests ont permis d'établir que le père de Toutankhamon était le pharaon Akhenaton, qui a régné entre 1351 et 1334 avant Jésus-Christ.\n\n\nAkhenaton était l'époux de la légendaire reine Néfertiti.\n\n\nPour autant, celle-ci n'est pas la mère de Toutankhamon. La mère du jeune pharaon, dont la momie a été retrouvée, serait la soeur de son père. L'analyse génétique montre en effet une consanguinité entre les parents.\n\n\nToutankhamon aurait épousé sa demi-soeur, Ankhsenpaamon. Le mariage entre frère et soeur était commun dans l'Egypte des pharaons.\n\n\nLe couple n'a pas de descendance connue mais deux momies d'enfants mort-nés ont toutefois été découvertes dans la tombe du jeune roi.\n\n\n- Un règne troublé, une mort mystérieuse -\n\n\nC'est à neuf ans, vers 1333 avant Jésus-Christ, que Toutankhamon serait monté sur le trône de Haute et Basse Egypte, mais les âges et les dates varient d'un spécialiste à l'autre.\n\n\nLe pays sort alors d'une période troublée, marquée par la volonté d'Akhenaton d'instaurer une forme de monothéisme dédiée au dieu du soleil Aton.\n\n\nL'arrivée au pouvoir du jeune prince permet aux tenants du culte d'Amon de reprendre le dessus et de rétablir les divinités traditionnelles.\n\n\nPlusieurs théories ont circulé sur les causes de son décès: maladie, accident de char ou meurtre.\n\n\nEn 2010, des tests génétiques et des études radiologiques ont révélé que l'adolescent serait en fait mort de paludisme combiné à une affection osseuse. Le jeune roi boitait d'un pied en raison d'une nécrose osseuse et son système immunitaire était déficient.\n\n\n- Un trésor maudit ? -\n\n\nQuelques mois après la fabuleuse découverte, le mythe de la malédiction du pharaon, qui frapperait ceux qui ont ouvert le tombeau, prend corps lorsque Lord Carnavon meurt en avril 1923 de septicémie, après une coupure infectée.\n\n\nLa légende se nourrit aussi d'une série de décès, comme celui de Carter qui meurt d'un cancer en 1939 à l'âge de 64 ans sans avoir achevé la publication de son ouvrage sur la sépulture, alors qu'il avait consacré dix ans à répertorier le trésor.\n\n\nAgatha Christie s'inspirera de la malédiction de Toutankhamon pour une de ses célèbres nouvelles: \"L'aventure du tombeau égyptien\".\n\n\nbur-kd-ays/mw/sbh/roc",
            sentences=[
                Sentence(start=0,
                         end=230
                         ),
                Sentence(start=233,
                         end=582
                         ),
                Sentence(start=585,
                         end=738
                         ),
                Sentence(start=741,
                         end=893
                         ),
                Sentence(start=896,
                         end=1019
                         ),
                Sentence(start=1022,
                         end=1232
                         ),
                Sentence(start=1235,
                         end=1415
                         ),
                Sentence(start=1418,
                         end=1630
                         ),
                Sentence(start=1633,
                         end=1810
                         ),
                Sentence(start=1813,
                         end=1870
                         ),
                Sentence(start=1873,
                         end=1929
                         ),
                Sentence(start=1930,
                         end=2015
                         ),
                Sentence(start=2016,
                         end=2088
                         ),
                Sentence(start=2091,
                         end=2147
                         ),
                Sentence(start=2148,
                         end=2220
                         ),
                Sentence(start=2223,
                         end=2356
                         ),
                Sentence(start=2359,
                         end=2583
                         ),
                Sentence(start=2586,
                         end=2731
                         ),
                Sentence(start=2734,
                         end=2874
                         ),
                Sentence(start=2877,
                         end=2974
                         ),
                Sentence(start=2977,
                         end=3128
                         ),
                Sentence(start=3129,
                         end=3235
                         ),
                Sentence(start=3238,
                         end=3258
                         ),
                Sentence(start=3259,
                         end=3490
                         ),
                Sentence(start=3493,
                         end=3738
                         ),
                Sentence(start=3741,
                         end=3896
                         )
            ],
            metadata={"language": "fr"},
        ),
        Document(
            identifier="1",
            text="Emmanuel Macron est le président de la France et Elizabeth Borne est la première-ministre de la France",
            sentences=[
                Sentence(
                    start=0,
                    end=102
                ),
            ],
            metadata={"language": "fr"},
        ),
    ]
    docs = processor.process(docs, parameters)
    assert docs == HasLen(2)
    doc0 = docs[0]
    for a in doc0.annotations:
        assert a.text == doc0.text[a.start:a.end]


@pytest.fixture
def expected_en():
    return {
        "Sport": "The french team is going to win Euro 2021 football tournament",
        "Politics": "Who are you voting for in 2021?",
        "Science": "Coronavirus vaccine research are progressing",
    }


@pytest.mark.skip(reason="Not a test")
def test_function_call_cat(expected_en):
    candidate_labels = {
        'sport': 'Sport',
        'politics': 'Politics',
        'science': 'Science',
    }

    prompt = """You are an expert Text Classification system. Your task is to accept Text as input and provide a category for the text based on the predefined labels.
{%- set labels=[] -%}
{%- for l in parameters.candidate_labels.values() -%}
  {%- do labels.append('"' + l + '"') -%}
{%- endfor %}
Classify the text below to one of the following labels: {{ labels|join(', ') }}
The task is exclusive, so only choose one label from what I provided.
Text: {{doc.text}}
"""

    parameters = OpenAICompletionParameters(
        model=OpenAIModel.gpt_3_5_turbo,
        completion_altText=None,
        prompt=prompt,
        function=OpenAIFunction.add_exclusive_category,
        candidate_labels=candidate_labels
    )
    processor = OpenAICompletionProcessor()
    docs = [Document(text=t) for t in expected_en.values()]
    docs = processor.process(docs, parameters)
    for expected_label, doc in zip(expected_en.keys(), docs):
        assert doc.categories[0].label == expected_label

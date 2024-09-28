# %%
import requests
import re

# %%
def famlyFeedGet(session, params, accesstoken):
    resp = session.get(
        'https://app.famly.co/api/feed/feed/feed',
        params=params, 
        headers={
            'x-famly-accesstoken': accesstoken
        })
    resp.raise_for_status()
    return resp.json()

def famlyObservationGet(session, id, accesstoken):
    resp = session.post(
        'https://app.famly.co/graphql?ObservationsByIds',
        json={
            "operationName": "ObservationsByIds",
            "variables": {
                "observationIds": [
                    id
                ]
            },
            "query": 'query ObservationsByIds($observationIds: [ObservationId!]!) {\n  childDevelopment {\n    observations(first: 100, observationIds: $observationIds, ignoreMissing: true) {\n      results {\n        ...ObservationData\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ObservationData on Observation {\n  ...ObservationDataWithNoComments\n  comments {\n    count\n    results {\n      ...Comment\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment Comment on Comment {\n  behaviors {\n    id: behaviorId\n    __typename\n  }\n  body\n  id\n  likes {\n    count\n    likedByMe\n    likes {\n      ...Like\n      __typename\n    }\n    __typename\n  }\n  sentAt\n  sentBy {\n    name {\n      fullName\n      __typename\n    }\n    profileImage {\n      url\n      __typename\n    }\n    __typename\n  }\n  canReport\n  __typename\n}\n\nfragment Like on Like {\n  likedAt\n  reaction\n  likedBy {\n    profileImage {\n      url\n      __typename\n    }\n    name {\n      firstName\n      fullName\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ObservationDataWithNoComments on Observation {\n  children {\n    id\n    name\n    institutionId\n    profileImage {\n      url\n      __typename\n    }\n    __typename\n  }\n  id\n  version\n  feedItem {\n    id\n    __typename\n  }\n  createdBy {\n    name {\n      fullName\n      __typename\n    }\n    profileImage {\n      url\n      __typename\n    }\n    __typename\n  }\n  status {\n    state\n    createdAt\n    __typename\n  }\n  variant\n  settings {\n    assessmentSetting {\n      assessmentSettingsId\n      title\n      __typename\n    }\n    __typename\n  }\n  behaviors {\n    id: behaviorId\n    ... on BehaviorCanLinkToFrameworks {\n      ...BehaviorCanLinkToFrameworks\n      __typename\n    }\n    ... on BehaviorObservationVariantAmbiguity {\n      variants\n      __typename\n    }\n    __typename\n  }\n  remark {\n    id\n    body\n    richTextBody\n    date\n    statements {\n      refinement\n      statement {\n        body\n        id\n        area {\n          frameworkId\n          id\n          lower\n          upper\n          title\n          abbr\n          color\n          deletedAt\n          subAreas {\n            title\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    areas {\n      area {\n        frameworkId\n        id\n        parentId\n        title\n        description\n        abbr\n        color\n        placement\n        deletedAt\n        framework {\n          id\n          title\n          owner\n          __typename\n        }\n        __typename\n      }\n      refinement\n      note\n      areaRefinementSettings {\n        ageBandSetting {\n          ...AgeBandSetting\n          __typename\n        }\n        assessmentOptionSetting {\n          ...AssessmentOptionSetting\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    customFieldValues {\n      customFieldSetting {\n        assessmentSettingsId\n        customFieldId\n        label\n        order\n        __typename\n      }\n      value\n      __typename\n    }\n    __typename\n  }\n  nextStep {\n    id\n    body\n    richTextBody\n    __typename\n  }\n  files {\n    name\n    url\n    id\n    __typename\n  }\n  images {\n    height\n    width\n    id\n    secret {\n      crop\n      expires\n      key\n      path\n      prefix\n      __typename\n    }\n    __typename\n  }\n  videos {\n    ... on TranscodingVideo {\n      id\n      __typename\n    }\n    ... on TranscodedVideo {\n      duration\n      height\n      id\n      thumbnailUrl\n      videoUrl\n      width\n      __typename\n    }\n    __typename\n  }\n  likes {\n    count\n    likedByMe\n    reactedByMe\n    likes {\n      ...Like\n      __typename\n    }\n    __typename\n  }\n  canReport\n  __typename\n}\n\nfragment BehaviorCanLinkToFrameworks on BehaviorCanLinkToFrameworks {\n  id: behaviorId\n  __typename\n  frameworks {\n    ...MinimalFramework\n    __typename\n  }\n}\n\nfragment MinimalFramework on Framework {\n  id\n  title\n  abbr\n  areas {\n    title\n    description\n    abbr\n    color\n    id\n    __typename\n  }\n  __typename\n}\n\nfragment AgeBandSetting on AgeBandSetting {\n  ageBandSettingId\n  id: ageBandSettingId\n  assessmentSettingsId\n  from\n  to\n  label\n  __typename\n}\n\nfragment AssessmentOptionSetting on AssessmentOptionSetting {\n  assessmentOptionSettingId\n  id: assessmentOptionSettingId\n  assessmentSettingsId\n  backgroundColor\n  fontColor\n  label\n  __typename\n}'
        },
        headers={
            'x-famly-accesstoken': accesstoken
        }
    )
    resp.raise_for_status()
    return resp.json()

# %% Get all the observation IDs by working our way back through the feed
session = requests.Session()
with open('/run/secrets/famly_access_token') as secret:
    accesstoken = secret.readline()
observationIds = []
createdDates = []
content = famlyFeedGet(
    session,
    {'heightTarget': 547}, 
    accesstoken
)
while len(content.get('feedItems', [])) > 0:
    observationIds.extend([item.get('embed', {}).get('observationId') for item in content.get('feedItems', []) if item.get('embed', {}) is not None and item.get('embed', {}).get('type') == 'Observation'])
    createdDates.extend([item.get('createdDate') for item in content.get('feedItems', [])])
    content = famlyFeedGet(
        session,
        {'olderThan': createdDates[-1], 'heightTarget': 547}, 
        accesstoken
    )
    print(createdDates[-1])

# %% Get the individual observations by ID and then the image URLs
downloads = {}
for id in observationIds:
    content = famlyObservationGet(session, id, accesstoken)
    images = [result.get('images') for result in content.get('data').get('childDevelopment').get('observations').get('results')]
    downloads = downloads | {image.get('secret').get('path'): f'{image.get('secret').get('prefix')}/{image.get('secret').get('key')}/{image.get('width')}x{image.get('height')}/{image.get('secret').get('path')}?expires={image.get('secret').get('expires')}' for image in images[0]}

# %% Download the images from the URLs
for name, url in downloads.items():
    fname = re.sub('images-', '', re.sub('archive-', '', re.sub('/', '-', name)))
    resp = session.get(url, stream=True)
    with open(fname, 'wb') as fd:
        for chunk in resp.iter_content(chunk_size=128):
            fd.write(chunk)

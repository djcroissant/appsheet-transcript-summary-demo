export TOKEN=$(gcloud auth print-access-token)
#export GOOGLE_CLOUD_PROJECT=$(gcloud config get project)

export COUNTER=0

while [ $COUNTER -le 1 ]
do
    RESULT=$(curl --location --request POST "https://firestore.googleapis.com/v1/projects/$GOOGLE_CLOUD_PROJECT/databases/(default)/documents/transcripts?documentId=b420fdb" \
    --header "Authorization: Bearer $TOKEN" \
    --header "Content-Type: application/json" \
    --data-raw "{
        'fields': {
            'id': {
                'stringValue': 'b420fdb'
            },
            'docText': {
                'stringValue': 'Transcript of entire conversation'
            },
            'dateTime': {
                'stringValue': '8/9/2023 9:38:51 AM'
            },
            'docSummary': {
                'stringValue': 'Summary of doc from text bison'
            },
            'docId': {
                'stringValue': '1PNXEjDP00Qs-nUIKa1XuTrFvpYrL7anlwgHjyUh-Aqw'
            }
        }
    }")

    echo $RESULT

    if [[ "$RESULT" == *error* ]]
    then
        COUNTER=$(( $COUNTER + 1 ))
        echo "Error detected, waiting 10s and then retry $COUNTER of 10 tries..."
        sleep 10s
    else
        COUNTER=11
    fi

done
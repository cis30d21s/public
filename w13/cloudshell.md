# AWS IoT

## IoT Core Usage

Thing setup:

```bash
thingName=thing1
aws iot create-thing --thing-name cis30d21s-$thingName
aws iot list-things

aws iot create-keys-and-certificate --set-as-active \
    --certificate-pem-outfile $thingName-cert.pem \
    --public-key-outfile $thingName-pub.pem \
    --private-key-outfile $thingName-priv.pem
# amazon CAs: https://www.amazontrust.com/repository/
http https://www.amazontrust.com/repository/AmazonRootCA1.pem --download

accountId=$(aws sts get-caller-identity | jq -r .Account)
sed "s/%accountId%/$accountId/g" iot-policy.json > .iot-policy.json
aws iot create-policy --policy-name cis30d21s --policy-document file://.iot-policy.json
certificateArn=$(aws iot list-certificates | jq -r '.certificates[0].certificateArn')
aws iot attach-principal-policy --principal $certificateArn --policy-name cis30d21s
aws iot attach-thing-principal --thing-name cis30d21s-$thingName --principal $certificateArn
aws iot describe-endpoint --endpoint-type iot:Data-ATS
```

Policy updates:

```bash
# update policy
sed "s/%accountId%/$accountId/g" iot-policy.json > .iot-policy.json
aws iot create-policy-version --policy-name cis30d21s --policy-document file://.iot-policy.json --set-as-default

# delete last policy version
lastVersion=$(aws iot list-policy-versions --policy-name cis30d21s | jq -r '.policyVersions[-1].versionId')
aws iot delete-policy-version --policy-name cis30d21s --policy-version-id $lastVersion
```

## Device Shadows

Create IAM user for JS client:

```bash
accountId=$(aws sts get-caller-identity | jq -r .Account)
sed "s/%accountId%/$accountId/g" iot-policy-web.json > .iot-policy-web.json
aws iam create-user --path /iot/ --user-name cis30d21s-iot-web
aws iam put-user-policy --user-name cis30d21s-iot-web --policy-name cis30d21s-iot-web --policy-document file://.iot-policy-web.json
aws iam create-access-key --user-name cis30d21s-iot-web
```

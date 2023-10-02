import {rpcClient, RPCHTTPClient} from "jsonrpc2-tsclient";

import {Vector3, PydanticTypes, PydanticNetworkTypes, PydanticExtra, PaymentCardBrand, Constantly, Primitives, VanillaModel, RecursiveModel, PythonTypes, Flavor, Numbers, Defaults, CollectionsModel, ConstrainedCollections} from "./models.js";

const transport = new RPCHTTPClient("http://localhost:8000/api/v1");

@rpcClient(
  transport,
  "",
  [
  
  ],
  {

  }
)
export class TabellaDemoClient {

  public math: TabellaDemoMathClient;
  public auth: TabellaDemoAuthClient;
  public extra: TabellaDemoExtraClient;

  constructor(headers: object = {}) {
    transport.headers = headers;
    this.math = new TabellaDemoMathClient();
    this.auth = new TabellaDemoAuthClient();
    this.extra = new TabellaDemoExtraClient();
  }

  public async httpOnlyMethod(
  // @ts-ignore
  ): Promise<null> {}
  public async wsOnlyMethod(
  // @ts-ignore
  ): Promise<null> {}
  public async wait(
    seconds: number  // @ts-ignore
  ): Promise<number> {}
  public async wait5(
  // @ts-ignore
  ): Promise<null> {}
  public async waitSum(
    a: number,    b: number  // @ts-ignore
  ): Promise<number> {}
  public async untyped(
    a: any,    b: any  // @ts-ignore
  ): Promise<any> {}
  public async undocumented(
    a: number,    b: number  // @ts-ignore
  ): Promise<number> {}
  public async constant(
    constStrField: string,    constNumField: number,    constNoneField: null,    constTrueField: boolean,    constFalseField: boolean  // @ts-ignore
  ): Promise<Constantly> {}
  public async primitives(
    a: number,    b: number,    c: string,    d: boolean,    e: string,    f: null  // @ts-ignore
  ): Promise<Primitives> {}
  public async models(
    a: VanillaModel,    b: RecursiveModel  // @ts-ignore
  ): Promise<[VanillaModel, RecursiveModel]> {}
  public async pythonTypes(
    strEnum: Flavor,    numEnum: Numbers,    date: string,    time: string,    datetimeField: string,    timedelta: string,    uuidField: string,    decimal: number | string  // @ts-ignore
  ): Promise<PythonTypes> {}
  public async default(
    a: string,    b: number,    c: number,    d: boolean,    e: boolean,    f: string[] | null  // @ts-ignore
  ): Promise<Defaults> {}
  public async defaultUntyped(
    g: any,    h: any,    i: any,    j: any,    k: any,    m: any  // @ts-ignore
  ): Promise<[any, any, any, any, any, any]> {}
  public async defaultEnum(
    a: Flavor,    b: any  // @ts-ignore
  ): Promise<[Flavor, any]> {}
  public async enumMethod(
    flavor: Flavor  // @ts-ignore
  ): Promise<Flavor> {}
  public async collectionsFunction(
    listField: any[],    listStr: string[],    listList: any[][],    listListInt: number[][],    listModel: VanillaModel[],    listModelOrModel: Array<VanillaModel | RecursiveModel>,    listUnion: Array<string | number>,    listDict: object[],    listDictStr: Record<string, string>[],    listDictIntKeys: Record<string, string>[],    tupleField: any[],    tupleStr: [string],    tupleTuple: [any[]],    tupleTupleInt: [[number]],    tupleModel: [VanillaModel],    tupleUnion: [string | number],    tupleIntStrNone: [number, string, null],    setStr: Set<string>,    setUnion: Set<string | number>,    dictField: object,    dictStr: Record<string, string>,    dictDict: Record<string, object>,    dictIntKeys: Record<string, string>,    dictModel: Record<string, VanillaModel>,    dictModelOrModel: Record<string, VanillaModel | RecursiveModel>,    dictUnion: Record<string, string | number>,    dictList: Record<string, number[]>  // @ts-ignore
  ): Promise<CollectionsModel> {}
  public async constrainedCollection(
    listMin: any[],    listMax: string[],    listMinMax: string[]  // @ts-ignore
  ): Promise<ConstrainedCollections> {}
  public async unions(
    unionParam: number | boolean | null  // @ts-ignore
  ): Promise<number | boolean | null> {}
  public async tupleMethod(
    a: [number | null, string, string]  // @ts-ignore
  ): Promise<[number | null, string, string]> {}
  public async anyArray(
    a: any[]  // @ts-ignore
  ): Promise<any[]> {}
  public async array(
    a: Array<number | null>  // @ts-ignore
  ): Promise<Array<number | null>> {}
  public async arrayArray(
    a: Array<Array<number | null>>  // @ts-ignore
  ): Promise<Array<Array<number | null>>> {}
  public async arrayUnionArray(
    a: Array<Array<any[] | number>>  // @ts-ignore
  ): Promise<Array<Array<any[] | number>>> {}
  public async objects(
    a: object  // @ts-ignore
  ): Promise<object> {}
  public async typedObject(
    a: Record<string, number | Flavor | null>  // @ts-ignore
  ): Promise<Record<string, number | Flavor | null>> {}
  public async objectObject(
    a: Record<string, Record<string, string>>  // @ts-ignore
  ): Promise<Record<string, Record<string, string>>> {}
  public async arrayModel(
    a: VanillaModel[]  // @ts-ignore
  ): Promise<VanillaModel[]> {}
  public async arrayRecursiveModel(
    a: RecursiveModel[]  // @ts-ignore
  ): Promise<RecursiveModel[]> {}
  public async topLevelUnionArray(
    a: boolean[] | null  // @ts-ignore
  ): Promise<boolean[] | null> {}
  public async unionArrays(
    a: boolean[] | number[] | string[]  // @ts-ignore
  ): Promise<boolean[] | number[] | string[]> {}

}

@rpcClient(
  transport,
  "",
  [
  ],
  {
    "add": "math.add",    "divide": "math.divide",    "subtract": "math.subtract",    "getDistance": "math.get_distance",    "getOrigin": "math.get_origin"
  }
)
class TabellaDemoMathClient {



  public async add(
    a: number,    b: number  // @ts-ignore
  ): Promise<number> {}
  public async divide(
    a: number,    b: number  // @ts-ignore
  ): Promise<number> {}
  public async subtract(
    a: number,    b: number  // @ts-ignore
  ): Promise<number> {}
  public async getDistance(
    a: Vector3,    b: Vector3  // @ts-ignore
  ): Promise<Vector3> {}
  public async getOrigin(
  // @ts-ignore
  ): Promise<Vector3> {}

}

@rpcClient(
  transport,
  "",
  [
  ],
  {
    "needsApiKey": "auth.needs_api_key",    "needsBearerToken": "auth.needs_bearer_token",    "needsOauthRead": "auth.needs_oauth_read",    "needsOauthWrite": "auth.needs_oauth_write",    "needsOauthReadWrite": "auth.needs_oauth_read_write",    "needsApikeyOrBearer": "auth.needs_apikey_or_bearer"
  }
)
class TabellaDemoAuthClient {



  public async needsApiKey(
  // @ts-ignore
  ): Promise<string> {}
  public async needsBearerToken(
  // @ts-ignore
  ): Promise<string> {}
  public async needsOauthRead(
  // @ts-ignore
  ): Promise<number> {}
  public async needsOauthWrite(
  // @ts-ignore
  ): Promise<boolean> {}
  public async needsOauthReadWrite(
  // @ts-ignore
  ): Promise<number> {}
  public async needsApikeyOrBearer(
  // @ts-ignore
  ): Promise<boolean> {}

}

@rpcClient(
  transport,
  "",
  [
  ],
  {
    "pydanticTypes": "extra.pydantic_types",    "pydanticNetworkTypes": "extra.pydantic_network_types",    "pydanticExtra": "extra.pydantic_extra"
  }
)
class TabellaDemoExtraClient {



  public async pydanticTypes(
    strictBool: boolean,    positiveInt: number,    negativeInt: number,    nonPositiveInt: number,    nonNegativeInt: number,    strictInt: number,    positiveFloat: number,    negativeFloat: number,    nonPositiveFloat: number,    nonNegativeFloat: number,    strictFloat: number,    finiteFloat: number,    strictBytes: string,    strictStr: string,    uuid1: string,    uuid3: string,    uuid4: string,    uuid5: string,    base64Bytes: string,    base64Str: string,    strConstraintsStripWhitespace: string,    strConstraintsToUpper: string,    strConstraintsToLower: string,    strConstraintsStrict: string,    strConstraintsMinLength: string,    strConstraintsMaxLength: string,    jsonField: string,    pastDate: string,    futureDate: string,    awareDatetime: string,    naiveDatetime: string,    pastDatetime: string,    futureDatetime: string,    constrainedFloat: number  // @ts-ignore
  ): Promise<PydanticTypes> {}
  public async pydanticNetworkTypes(
    anyUrl: string,    anyHttpUrl: string,    httpUrl: string,    postgresDsn: string,    cockroachDsn: string,    amqpDsn: string,    redisDsn: string,    mongoDsn: string,    kafkaDsn: string,    mysqlDsn: string,    mariadbDsn: string,    emailStr: string,    nameEmail: string,    ipvAnyAddress: string,    ipvAnyInterface: string,    ipvAnyNetwork: string  // @ts-ignore
  ): Promise<PydanticNetworkTypes> {}
  public async pydanticExtra(
    color: string,    paymentCardBrand: PaymentCardBrand,    paymentCardNumber: string,    abaRoutingNumber: string  // @ts-ignore
  ): Promise<PydanticExtra> {}

}


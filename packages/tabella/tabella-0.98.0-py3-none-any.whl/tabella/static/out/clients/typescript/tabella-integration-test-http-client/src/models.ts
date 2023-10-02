

export enum PaymentCardBrand {
    AMERICAN_EXPRESS = "American Express",
    MASTERCARD = "Mastercard",
    VISA = "Visa",
    MIR = "Mir",
    OTHER = "other",
}

export enum Flavor {
    MOCHA = "mocha",
    VANILLA = "vanilla",
    PEPPERMINT = "peppermint",
}

export enum Numbers {
    NUMBER_1 = 1,
    NUMBER_2 = 2,
    NUMBER_3 = 3,
}


export interface Vector3 {
    x: number
    y: number
    z: number
}

export interface PydanticTypes {
    strictBool: boolean
    positiveInt: number
    negativeInt: number
    nonPositiveInt: number
    nonNegativeInt: number
    strictInt: number
    positiveFloat: number
    negativeFloat: number
    nonPositiveFloat: number
    nonNegativeFloat: number
    strictFloat: number
    finiteFloat: number
    strictBytes: string
    strictStr: string
    uuid1: string
    uuid3: string
    uuid4: string
    uuid5: string
    base64Bytes: string
    base64Str: string
    strConstraintsStripWhitespace: string
    strConstraintsToUpper: string
    strConstraintsToLower: string
    strConstraintsStrict: string
    strConstraintsMinLength: string
    strConstraintsMaxLength: string
    jsonField: string
    pastDate: string
    futureDate: string
    awareDatetime: string
    naiveDatetime: string
    pastDatetime: string
    futureDatetime: string
    constrainedFloat: number
}

export interface PydanticNetworkTypes {
    anyUrl: string
    anyHttpUrl: string
    httpUrl: string
    postgresDsn: string
    cockroachDsn: string
    amqpDsn: string
    redisDsn: string
    mongoDsn: string
    kafkaDsn: string
    mysqlDsn: string
    mariadbDsn: string
    emailStr: string
    nameEmail: string
    ipvAnyAddress: string
    ipvAnyInterface: string
    ipvAnyNetwork: string
}

export interface PydanticExtra {
    color: string
    paymentCardBrand: PaymentCardBrand
    paymentCardNumber: string
    abaRoutingNumber: string
}

export interface KineticBody {
    position: Vector3
    velocity: Vector3
    mass: number
}

export interface VanillaModel {
    boolField: boolean
}

export interface RecursiveModel {
    value: number
    child: RecursiveModel | null
}

export interface Constantly {
    constStrField: string
    constNumField: number
    constNoneField: null
    constTrueField: boolean
    constFalseField: boolean
}

export interface Primitives {
    intField: number
    floatField: number
    strField: string
    boolField: boolean
    bytesField: string
    noneField: null
}

export interface PythonTypes {
    strEnum: Flavor
    numEnum: Numbers
    date: string
    time: string
    datetimeField: string
    timedelta: string
    uuidField: string
    decimal: number | string
    path: string
}

export interface DefaultFactory {
    id: string
}

export interface Defaults {
    strField: string
    intField: number
    floatField: number
    boolTrue: boolean
    boolFalse: boolean
    listField: string[] | null
    childField: DefaultFactory | null
}

export interface CollectionsModel {
    listField: any[]
    listStr: string[]
    listList: any[][]
    listListInt: number[][]
    listModel: VanillaModel[]
    listModelOrModel: Array<VanillaModel | RecursiveModel>
    listUnion: Array<string | number>
    listDict: object[]
    listDictStr: Record<string, string>[]
    listDictIntKeys: Record<string, string>[]
    tupleField: any[]
    tupleStr: [string]
    tupleTuple: [any[]]
    tupleTupleInt: [[number]]
    tupleModel: [VanillaModel]
    tupleUnion: [string | number]
    tupleIntStrNone: [number, string, null]
    setStr: Set<string>
    setUnion: Set<string | number>
    dictField: object
    dictStr: Record<string, string>
    dictDict: Record<string, object>
    dictIntKeys: Record<string, string>
    dictModel: Record<string, VanillaModel>
    dictModelOrModel: Record<string, VanillaModel | RecursiveModel>
    dictUnion: Record<string, string | number>
    dictList: Record<string, number[]>
}

export interface ConstrainedCollections {
    listMin: any[]
    listMax: string[]
    listMinMax: string[]
}

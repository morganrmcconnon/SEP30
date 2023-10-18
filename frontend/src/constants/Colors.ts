//Stores colours for usage in Vis components

const white = getComputedStyle(document.body).getPropertyValue('--color-white')

export const ColorVar = {
    white: white,
    blue: "#339AF0",
    lightblue: "#D0EBFF",
    green: "#51CF66",
    lightgreen: "#D3F9D8",
    red: "#FF6B6B",
    lightred:"#FFCCCC",
    orange: "#FF922B",
}

export const ColorMap = {
    topic: ColorVar.blue,
    keyword: ColorVar.green,
    positive: ColorVar.green,
    neutral: ColorVar.blue,
    negative: ColorVar.orange,
    "<=18": ColorVar.blue,
    "19-29": ColorVar.green,
    "30-39": ColorVar.orange,
    ">=40": ColorVar.red,
    female: {
        normal: ColorVar.red,
        light: ColorVar.lightred,
    },
    male: {
        normal: ColorVar.blue,
        light: ColorVar.lightblue,
    },
}

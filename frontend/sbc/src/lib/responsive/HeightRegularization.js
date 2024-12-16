export function updateScreenHeight(screenHeight, maxHeight){
    if(screenHeight.value <= 700){
        return maxHeight.value = 58
    }
    if(screenHeight.value <= 850){
        return maxHeight.value = 73
    }
    if(screenHeight.value <= 1000){
        return maxHeight.value = 78
    }
    if(screenHeight.value <= 1200){
        return maxHeight.value = 83
    }
    if(screenHeight.value <= 1300){
        return maxHeight.value = 88
    }
}
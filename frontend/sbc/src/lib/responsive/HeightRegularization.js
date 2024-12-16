export function updateScreenHeight(screenHeight, maxHeight){
    if(screenHeight.value <= 700){
        return maxHeight.value = 56
    }
    if(screenHeight.value <= 850){
        return maxHeight.value = 70
    }
    if(screenHeight.value <= 1000){
        return maxHeight.value = 76
    }
    if(screenHeight.value <= 1200){
        return maxHeight.value = 81
    }
    if(screenHeight.value <= 1300){
        return maxHeight.value = 86
    }
}
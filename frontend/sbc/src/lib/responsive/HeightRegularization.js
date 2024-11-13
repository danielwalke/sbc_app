export function updateScreenHeight(screenHeight, maxHeight){
    if(screenHeight.value <= 700){
        return maxHeight.value = 60
    }
    if(screenHeight.value <= 850){
        return maxHeight.value = 70
    }
    if(screenHeight.value <= 1000){
        return maxHeight.value = 75
    }
    if(screenHeight.value <= 1200){
        return maxHeight.value = 80
    }
    if(screenHeight.value <= 1300){
        return maxHeight.value = 85
    }
}
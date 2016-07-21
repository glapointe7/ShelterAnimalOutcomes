library(lubridate)
library(stringr)
library(xgboost)
#library(methods)
library(Matrix)
#library(gridExtra)
library(ggplot2)
library(scales)
#library(data.table)
library(plyr)
library(dplyr)
library(MLmetrics)
library(Ckmeans.1d.dp)
library(caret)


CategoryToInteger <- function(feature)
{
    feature.categories <- unique(feature)
    feature.categories.id <- 1:length(feature.categories)
    names(feature.categories.id) <- as.vector(feature.categories)
    feature <- feature.categories.id[feature]
    
    return(feature)
}


GetBooleanFeatureFromGroup <- function(feature, group)
{
    indices <- grep(group, feature)
    feature.is.bool <- rep(0, length(feature))
    feature.is.bool[indices] <- 1
    
    return(feature.is.bool)
}


GetIntegerFeatureFromGroups <- function(feature, groups)
{
    feature.group <- rep(0, length(feature))
    i <- 1
    for(group in groups)
    {
        indices <- grep(group, feature)
        feature.group[indices] <- i
        i <- i + 1
    }
    
    return(feature.group)
}

# 
# CreateDataframeFromThreshold <- function(prediction, threshold)
# {
#     prediction.ncol <- ncol(prediction)
#     x <- apply(prediction, 1, function(x) which(x >= threshold))
#     for(i in 1:length(x))
#     {
#         if(length(x[[i]]) > 0)
#         {
#             row <- rep(0, prediction.ncol)
#             row[x[[i]][[1]]] <- 1
#             prediction[i, ] <- row
#         }
#     }
#     
#     return(prediction)
# }
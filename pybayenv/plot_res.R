#!/usr/bin/Rscript
args <- commandArgs(trailingOnly = TRUE)
bin <- args[1] #Binary matrix with results
avg <- args[2] #Average BF
med <- args[3] #Median BF
tau <- strtoi(args[4]) #the number of tests
env <- args[5] #The environmental number

bin <- read.table(bin, header=F, sep="\t")
avg_bf <- read.table(avg, header=F, sep="\t")
median_bf <- read.table(med, header=F, sep="\t")
avg_bf$total <- bin$V34
avg_bf$median <- median_bf$V2
kappa <- 0.7 #cutoff percentage

cutoff <- tau*kappa

sorted_bf <- avg_bf[order(avg_bf$total, decreasing=TRUE),]

postscript(paste(env, "significance-plot.eps", sep=""), horizontal=FALSE)
plot(sorted_bf$total, type="o", xlab="Markers",lwd=2, ylab="Times identified",col="black", main="Staha seed system stages, tau=32, kappa=0.7")
#lines(log10(sorted_bf$V2), col="red", lwd=1)
#lines(log10(sorted_bf$median), col="blue", lwd=1)
#lines(sorted_bf$V2, col="green", lwd=1)
#lines(sorted_bf$median, col="blue", lwd=1)
#legend(80,30, c("Times identified","log10 Average BF", "log10 Median BF"), lty=c(1,1,1),lwd=c(2,1,1),col=c("black","green", "blue"))
#legend(22,30, c("Times identified","Average BF", "Median BF"), lty=c(1,1,1),lwd=c(2,1,1),col=c("black","green", "blue"))
abline(h=cutoff, col="red", lty="dashed")
dev.off()

# print(data)
# print(iter)
# res <- read.table(data, header=TRUE)
# attach(res)
# orderChr <- res[order(chr),]
# orderMin <- res[order(Temp_Min, decreasing=TRUE),]
# orderMax <- res[order(Temp_Max, decreasing=TRUE),]
# orderPre <- res[order(Precip, decreasing=TRUE),]
# detach(res)
# attach(orderChr)
# postscript(paste(iter, "iterMin.eps", sep=""), horizontal=FALSE)
# plot(Temp_Min, col=chr, main="BF Temp_Min coloured by chromosome", pch=16)
# dev.off()

# postscript(paste(iter, "iterMax.eps", sep=""), horizontal=FALSE)
# plot(Temp_Max, col=chr, main="BF Temp_Max coloured by chromosome", pch=16)
# dev.off()

# postscript(paste(iter, "iterPre.eps", sep=""), horizontal=FALSE)
# plot(Precip, col=chr, main="BF Precip coloured by chromosome", pch=16)
# dev.off()
# detach(orderChr)

# write.table(head(orderMin, 35), file = paste(iter, "orderMin.txt", sep=""), sep = "\t")
# write.table(head(orderMax, 35), file = paste(iter, "orderMax.txt", sep=""), sep = "\t")
# write.table(head(orderPre, 35), file = paste(iter, "orderPre.txt", sep=""), sep = "\t")


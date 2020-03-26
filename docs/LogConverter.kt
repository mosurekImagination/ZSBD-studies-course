import java.io.File

fun main(args: Array<String>) {
    val logPath = args.takeIf { it.isNotEmpty() }?.get(0)?.takeIf { it != "default" } ?: "stats.log"
    val resultPath = args.takeIf { it.isNotEmpty() && it.size == 2 }?.get(1)?.takeIf { it != "default" } ?: "results"

    var tableExists = false
    var transactionNumber = 1
    var queryNumber = 1

    val newFile = File("$resultPath.md")
    val stringBuffer = StringBuffer()

    val log = File(logPath).readLines()
    for (line in log.indices - 1) {
        with(log[line]) {
            when {
                takeLast(3) == "---" -> {
                    addCommonTable(stringBuffer, log[line + 1], transactionNumber)
                }
                isEmpty() -> {
                    tableExists = false
                }
                take(5) == "Query" -> {
                    when (tableExists) {
                        true -> addRowToTable(stringBuffer, log[line + 1], queryNumber++)
                        false -> {
                            queryNumber = 1
                            startNewTable(stringBuffer, transactionNumber++)
                            addRowToTable(stringBuffer, log[line + 1], queryNumber++)
                            tableExists = true
                        }
                    }
                }
            }
        }
    }

    newFile.writeText(stringBuffer.toString())
}

fun addCommonTable(buffer: StringBuffer, lineToAdd: String, transactionNumber: Int) {
    buffer.append("#### Transakcja $transactionNumber - srednie czasy \n")
    startNewTable(buffer, transactionNumber, withHeader = false)
    addRowToTable(buffer, lineToAdd, transactionNumber, withHeader = false)
}

fun addRowToTable(buffer: StringBuffer, lineToAdd: String, queryNumber: Int, withHeader: Boolean = true) {
    val prepared = lineToAdd.prepareToAdd()
    if (withHeader) {
        buffer.append("$queryNumber |")
    }
    buffer.append("$prepared  \n")
}

fun String.prepareToAdd(): String =
    split("|").map { it.trim() }.map { it.substring(IntRange(5, it.length - 1)) }.joinToString(" | ")

fun startNewTable(buffer: StringBuffer, transactionNumber: Int, withHeader: Boolean = true) {
    if (withHeader) buffer.append("#### Transakcja $transactionNumber \n Nr zapytania ")
    buffer.append("| Minimalny czas[s] | Maksymalny czas[s] | Średni czas[s] | \n")
    if (withHeader) buffer.append("| - ")
    buffer.append("| :--: | :--: | :--: | \n")
}
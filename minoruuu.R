library(shiny)
library(shinydashboard)
library(leaflet)
library(readr)
library(jpeg)
library(plotly)
library(lubridate)
library(wordcloud)
library(tm)
library(SnowballC)

ui <- fluidPage(
    headerPanel('HackEMTU 2018'),
    tabsetPanel(
        tabPanel('Usuario',
                 sidebarLayout(
                     sidebarPanel(
                         h5(HTML('<b>Avalie aqui:</b>')),
                         actionButton('bom', NULL, icon = icon('thumbs-up', class = NULL, lib = "font-awesome"), 385),
                         actionButton('ruim', NULL, icon = icon('thumbs-down', class = NULL, lib = "font-awesome"), 385),
                         textInput('rec', 'Descrição:', width = '600px'  ),
                         actionButton('walk', 'Atualizar mapa', width = 385),
                         fileInput("img", "Seleciona a sua imagem", multiple = TRUE, accept = ".jpg")
                     ),
                     mainPanel(
                         leafletOutput('map')
                     )
                 )
        ),
        tabPanel('EMTU',
                 fluidRow(
                     column(4,
                            h4('Wordcloud dos comentários'),
                            plotOutput('wordcloud')
                     ),
                     column(4,
                            h4('Notas por tempo'),
                            textOutput('date'),
                            plotlyOutput('plotly', width = '400px'),
                            h4('Último Tweet'),
                            textOutput('tweet'),
                            textOutput('nota')
                     ),
                     column(4,
                            h4('Imagem enviada pelo usuario classificada'),
                            imageOutput("image")
                     )
                 )
        )
    )
    
)

server <- function(input, output) {
    cloud <- NULL
    plotly_data <- isolate(data.frame('time' = 1, 'n' = 1, 'm' = 1, 'o' = 1))
    plotly_data <- isolate(plotly_data[-1, ])
    observeEvent(input$walk, {
        system('python3 run_sent.py')
        sentimentos <- read_csv2('sentimentos.csv')
        output$tweet <- renderText(sentimentos$texto[nrow(sentimentos)])
        output$nota <- renderText(paste('Polaridade:', as.character(sentimentos$nota[nrow(sentimentos)])))
        ruim <- -input$ruim
        nota <- ruim + input$bom
        if(!is.na(sentimentos$nota)) nota <- nota + sum(as.numeric(sentimentos$nota))
        if(nota == 0){
            busIcon <- awesomeIcons(icon = 'ios-clos',
                                    iconColor = 'black',
                                    library = 'ion',
                                    markerColor = 'blue')
        }
        if(nota < 0) {
            busIcon <- awesomeIcons(icon = 'ios-clos',
                                    iconColor = 'black',
                                    library = 'ion',
                                    markerColor = 'red')
        }
        if(nota > 0){
            busIcon <- awesomeIcons(icon = 'ios-clos',
                                    iconColor = 'black',
                                    library = 'ion',
                                    markerColor = 'green')
        }
        system('python3 SMTU.py')
        coord <- read_csv(file = 'live_pos.csv')
        m <- leaflet() %>% 
            addTiles() %>%
            addAwesomeMarkers(lng = coord$lng[1],
                              lat = coord$lat[1],
                              icon = busIcon)
        output$map <- renderLeaflet(m)
        if(input$rec != ''){
            cloud <<- append(cloud, input$rec)
        }
            cloud <<- append(cloud, sentimentos$texto)
            auxCorpus <- Corpus(VectorSource(cloud))
            auxCorpus <- tm_map(auxCorpus, removePunctuation)
            auxCorpus <- tm_map(auxCorpus, removeWords, stopwords('pt'))
            auxCorpus <- tm_map(auxCorpus, removeWords, c('onibus', 'ônibus', 'Ônibus', 'emtu'))
            auxCorpus <- tm_map(auxCorpus, stemDocument)
            output$wordcloud <- renderPlot({
                wordcloud(auxCorpus, max.words=50, colors = c("blue", "red"), min.freq = 1)
            })

        output$date <- renderText(paste('Data:',
                                        paste(day(Sys.time()),
                                              month(Sys.time()),
                                              year(Sys.time()),
                                              sep = '/'),
                                        'Hora:',
                                        hour(Sys.time())))
        plotly_data <<- as.data.frame(rbind(plotly_data, c(minute(Sys.time()), input$ruim, input$bom, nota)))
        colnames(plotly_data) <- c('time', 'nota_ruim', 'nota_boa', 'total')
        
        output$plotly <- renderPlotly({
            plotly_data %>% ggplot(aes(x = time)) +
                geom_line(aes(y = nota_ruim), color = 'red') +
                geom_line(aes(y = nota_boa), color = 'green') +
                geom_line(aes(y = total), color = 'blue') +
                labs(x = 'Tempo', y = 'Nota', title = 'Notas por minuto')
        })
        
    })
    
    output$image <- renderImage({
        req(input$img)
        setwd("./darknet")
        system(paste('./darknet detect cfg/yolov3.cfg yolov3.weights', input$img$datapath))
        setwd("..")
        list(src = "darknet/predictions.png", width = 380)
    })
}

shinyApp(ui, server)
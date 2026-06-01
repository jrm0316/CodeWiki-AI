💻 CodeWiki AI                      
                        
CodeWiki AI é uma ferramenta de análise inteligente de código-fonte que utiliza IA Generativa, RAG (Retrieval-Augmented Generation) e busca vetorial para transformar projetos de software em documentação, explicações técnicas e conhecimento navegável.                  
O objetivo é permitir que desenvolvedores entendam rapidamente projetos novos ou existentes, reduzindo o tempo gasto explorando arquivos e código manualmente.                  
                                     
🚀 Principais Funcionalidades                  
📋 Visão Geral do Projeto                 
                                
Gera automaticamente um resumo completo do sistema analisado, explicando:                                   
➤ Objetivo do projeto                          
➤ Funcionalidades principais                            
➤ Estrutura geral                                   
➤ Componentes encontrados                              
                          
💬 Chat com o Código     
                
Faça perguntas em linguagem natural como:                                 
➤ "O que este projeto faz?"                     
➤ "Como funciona a autenticação?"                       
➤ "Onde é feita a conexão com o banco?"                      
➤ "Quais arquivos participam do upload?"                    
                          
A IA busca os trechos mais relevantes utilizando RAG e responde com base no código real do projeto.                     
                         
📚 Documentação Automática                     
                                
Geração automática de documentação para:                     
➤ Funções                         
➤ Classes                       
➤ Componentes encontrados                         
                          
Incluindo:                          
➤ Objetivo                       
➤ Parâmetros                       
➤ Retorno                          
➤ Fluxo de execução                          
➤ Possíveis melhorias                        
                             
🏗️ Explicação de Arquitetura                      
                                 
Analisa a estrutura do projeto e gera uma explicação arquitetural contendo:                   
➤ Organização dos módulos                         
➤ Responsabilidades dos arquivos                       
➤ Fluxo de dados                        
➤ Relações entre componentes                       
                           
🕸️ Mapa de Chamadas                         
                           
Exibe chamadas entre funções identificadas durante a análise do código.                             
Permite visualizar rapidamente como partes do sistema se conectam.                   
                          
🔗 Análise de Dependências                    
                                     
Detecta:                     
➤ Dependências internas do projeto                  
➤ Bibliotecas externas utilizadas                   
➤ Relações entre módulos                       
                                
🔍 Busca de Referências                        
                          
Permite localizar onde uma função, classe ou variável é utilizada dentro do projeto.                           
                        
🧭 Navegação Entre Funções                   
                     
Lista funções encontradas e permite:                     
Visualizar implementação                    
Gerar documentação                   
Localizar referências                        
                     
☠️ Detecção de Código Possivelmente Morto                   
                      
Identifica funções que aparentam não possuir chamadas dentro do projeto.                   
                          
Auxilia em:                   
➤ Refatoração                      
➤ Limpeza de código                
➤ Redução de complexidade                  
                   
📊 Diagramas e Relacionamentos                      
                    
Geração automática de diagramas Mermaid mostrando:                    
➤ Dependências                  
➤ Relações entre arquivos                      
➤ Estrutura do sistema                 
                           
📄 Exportação de Relatórios                       
                    
Geração automática de:                        
➤ README.md                       
➤ Relatórios PDF                      
➤ Documentação técnica                        
                          
🧠 Tecnologias Utilizadas                 
➤ Python                      
➤ Streamlit                 
➤ FAISS                    
➤ Sentence Transformers                  
➤ Groq API                  
➤ Llama 3.3 70B                     
➤ Mermaid                    
➤ ReportLab                      
                    
🔍 Como Funciona                      
1. O usuário envia um projeto compactado (.zip)                  
2. O sistema extrai os arquivos de código                
3. Os arquivos são divididos em blocos semânticos                
4. São gerados embeddings vetoriais                     
5. O índice FAISS é criado                   
6. A IA utiliza RAG para recuperar contexto relevante               
7. O usuário pode explorar, documentar e consultar o projeto              
                          
🌎 Linguagens Suportadas                  
                      
Atualmente o sistema possui foco principal em Python, mas já é capaz de analisar e gerar explicações para projetos contendo:            
➤ Python               
➤ Go                 
➤ JavaScript                   
➤ TypeScript                     
➤ Java                 
➤ C#                   
               
A análise semântica é realizada pela IA independentemente da linguagem utilizada.                    
                     
🎯 Objetivo do Projeto          
                   
O CodeWiki AI foi criado para transformar qualquer base de código em uma wiki inteligente, permitindo que desenvolvedores compreendam sistemas complexos de forma rápida e interativa.    
O projeto busca unir IA Generativa, RAG e análise de código para acelerar onboarding, documentação e manutenção de software.    
              
📌 Status do Projeto                    
                 
🚧 Em desenvolvimento ativo                   
              
Novas funcionalidades estão sendo adicionadas continuamente, incluindo melhorias na análise de arquitetura, documentação automática e suporte avançado a múltiplas linguagens.        

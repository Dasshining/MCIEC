Machine Learning

```plantuml
@startuml
' Styling to create circular/oval shapes
skinparam state {
    BackgroundColor White
    BorderColor DarkBlue
    ArrowColor DarkBlue
    FontName Helvetica
    ' High RoundCorner makes the rectangles look like ovals/circles
    RoundCorner 100 
}
skinparam shadowing false

title Relations: ML, NN, CNN, CV, and Pattern Recognition

' Main Hierarchy: ML > NN > CNN
state "Machine Learning (ML)" as ML {
    state "Neural Networks (NN)" as NN {
        state "Convolutional Neural\nNetworks (CNN)" as CNN
    }
}

' Pattern Recognition as the broad goal/field
state "Pattern Recognition (PR)" as PR

' Computer Vision as the specific application field
state "Computer Vision (CV)" as CV

' Connections (Fixed to use standard directional arrows)
' CNN is the tool for CV
CNN -right-> CV : "Primary Algorithm for"

' CV contributes to PR
CV -up-> PR : "Subset of (Visual)"

' ML provides methods for PR
ML -left-> PR : "Provides Algorithms"

' Theoretical intersection (Modelled as two arrows for bi-directionality)
PR --> ML : "Theoretical Intersection"

@enduml
```

```plantuml
Bob -> Alice : hello
Alice -> Wonderland: hello
Wonderland -> next: hello
next -> Last: hello
Last -> next: hello
next -> Wonderland : hello
Wonderland -> Alice : hello
Alice -> Bob: hello
```

```javascript  
function add(a, b) {  
return a + b;  
}  
```

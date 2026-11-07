```mermaid
erDiagram
    WRITERS ||--o{ SHOWS : writes
    SHOWS }o--o{ ACTORS : features

    WRITERS {
        string name
        int birthyear
    }

    SHOWS {
        string NAME
        int Year
        int ID
        int num_episodes
        string genre
        float rating
    }

    ACTORS {
        string name
        int birthyear
    }
```

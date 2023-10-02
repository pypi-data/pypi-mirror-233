# SearchSource: Pubmed

Note: This document is currently under development. It will contain the following elements.

- description
- coverage (disciplines, types of work)
- supported (details): run_search (including updates), load,  prep (including get_masterdata)

[Pubmed](https://pubmed.ncbi.nlm.nih.gov/)

## Add the search source

To add a pubmed API search, enter the query in the [Pubmed web interface](https://pubmed.ncbi.nlm.nih.gov/), run the search, copy the url and run:

```
colrev search -a colrev.pubmed -p "https://pubmed.ncbi.nlm.nih.gov/?term=fitbit"
```

## Links

- [Data field descriptions](https://www.nlm.nih.gov/bsd/mms/medlineelements.html)

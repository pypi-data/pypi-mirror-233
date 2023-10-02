<H1>BLK UTILS</H1>

A small utility library for my most commonly used functions across projects. 

<H2> Installation </H2>

`pip install blk-utils`

<H2> Example Usage </H2>

```
from blk_utils import get_relative_project_dir, cprint, ...

repo_name = 'my_repo'
project_dir = get_relative_project_dir(repo_name, partial=True)
data_dir = project_dir / 'data'

data_filepath = data_dir / 'my_table_data.csv'
df = pd.read_csv(data_filepath)
cprint(df)
```
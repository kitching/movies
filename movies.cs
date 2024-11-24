using System.Diagnostics;
using System.Text.RegularExpressions;

struct Movie
{
    public int Id { get; set; }
    public string Title { get; set; }
    public int Year { get; set; }
    public string Genres { get; set; }

    public override string ToString() => $"{Title} : {Year} : ({Genres})";
}

class Movies
{
    List<Movie> movieList = new List<Movie>();
    Dictionary<(int, string), HashSet<int>> movieDict = new Dictionary<(int, string), HashSet<int>>();
    HashSet<int> uniqueYears = new HashSet<int>();
    HashSet<string> uniqueGenres = new HashSet<string>();

    static void Main(string[] args)
    {
        var m = new Movies();
        m.Load();

        List<Movie> m1 = m.GetUniques("Animation", 2015, 2016);
        //m1.ForEach(x => Console.WriteLine(x));
        Console.WriteLine(string.Join(", ", m1));

        List<Movie> m2 = m.GetUniques("", 2012, 2012);
        //m2.ForEach(x => Console.WriteLine(x));
        Console.WriteLine(string.Join(", ", m2));

        m.TestSpeed();
    }

    public void Load()
    {
        using (var reader = new StreamReader("IMDB-Movie-Data.csv"))
        {
            var colIndices = new Dictionary<string, int>();
            int lineIndex = 0;
            while(!reader.EndOfStream)
            {
                string line = reader.ReadLine();
                // string[] values = line.Split(",");
                // ignore commas inside quotes and remove escaped quotes
                string[] values = Regex.Split(line, "[,]{1}(?=(?:[^\"]*\"[^\"]*\")*(?![^\"]*\"))").Select(x => x.Replace("\"", "")).ToArray();

                if (lineIndex == 0)
                {
                    // header row                   
                    colIndices = Enumerable.Range(0, values.Length).ToDictionary(x => values[x]); // indices are the values, values[x] are the keys
                }
                else
                {
                    // data row
                    int id = lineIndex - 1;
                    string title = values[colIndices["Title"]];
                    int year = int.Parse(values[colIndices["Year"]]);
                    string genres = values[colIndices["Genre"]];

                    var m = new Movie { Id = id, Title = title, Year = year, Genres = genres };
                    movieList.Add(m);

                    uniqueYears.Add(year);

                    foreach (string g in genres.Split(","))
                    {
                        (int, string) key = (year, g);

                        if (!movieDict.ContainsKey(key)) movieDict.Add(key, new HashSet<int>());
                        movieDict[key].Add(id);

                        uniqueGenres.Add(g);
                    }
                }

                lineIndex++;
            }
        }
    }

    public List<Movie> GetUniques(string genre, int fromYear, int toYear)
    {
        var uniques = new HashSet<int>();
        
        HashSet<int> yearQuery = new HashSet<int>(Enumerable.Range(fromYear, toYear+1-fromYear)); 
        yearQuery.IntersectWith(uniqueYears); // returns void, cannot chain

        List<string> genreQuery = String.IsNullOrEmpty(genre) ? new List<string>(uniqueGenres) : [genre];

        foreach (int y in yearQuery)
        {
            foreach(string g in genreQuery)
            {
                (int, string) key = (y, g);
                if (movieDict.TryGetValue(key, out var indices))
                    uniques.UnionWith(indices);
            }
        }

        return uniques.Select(x => movieList[x]).ToList();
    }

    public void TestSpeed()
    {
        var rnd = new Random();
        int trials = 100_000;
        double totalMs = 0;
        foreach (int i in Enumerable.Range(0, trials))
        {
            string genre = rnd.GetItems(uniqueGenres.ToArray(), 1).First();
            int yearFrom = rnd.GetItems(uniqueYears.ToArray(), 1).First();
            int yearTo = rnd.GetItems(uniqueYears.Where(x => x >= yearFrom).ToArray(), 1).First();

            Stopwatch s = Stopwatch.StartNew();
            List<Movie> m = GetUniques(genre, yearFrom, yearTo);            
            totalMs += s.Elapsed.TotalMilliseconds;
        }
        double avgMs = totalMs / trials;
        Console.WriteLine($"avg {avgMs} ms");
    }
}

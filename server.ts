import Client from './database-client';
import csv from 'csv-parser';
import fs from 'fs';

const arrayOf5000Strings: string[] = [];
fs.createReadStream('data/test.csv')
    .pipe(csv())
    .on('data', (row) => {
        arrayOf5000Strings.push(row.track_name);
    })
    .on('end', async () => {
        try {
            console.time();
            const { rows } = await getSimilarSongs(arrayOf5000Strings);
            console.timeEnd();

            const results: {
                [key: string]: { track_name: string; distance: number };
            } = {};

            for (const row of rows) {
                const { query_string, track_name, distance } = row;
                results[query_string] = { track_name, distance };
            }

            fs.writeFileSync(
                'data/postgres_trigram.json',
                JSON.stringify(results, null, 2)
            );
        } catch (error) {
            console.error('Error querying the database:', error);
        }
    });

async function getSimilarSongs(__arrayOf5000Strings: string[]) {
    const sql = `
        SELECT input.query_string,
            s.track_name,
            levenshtein(input.query_string, s.track_name, 2, 2, 3) AS distance
        FROM unnest($1::text[]) AS input(query_string)
        JOIN LATERAL (
            SELECT track_name
            FROM (
                SELECT track_name
                FROM songs
                WHERE track_name % input.query_string
                ORDER BY input.query_string <-> track_name, track_name
                LIMIT 100
            ) AS trigram_matches
            ORDER BY levenshtein(input.query_string, track_name, 2, 2, 3)
            LIMIT 1
        ) s ON true;
     `;
    const conn = await Client.connect();
    const result = await conn.query(sql, [__arrayOf5000Strings]);

    conn.release();

    return result;
}

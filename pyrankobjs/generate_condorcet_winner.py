{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "ename": "NameError",
     "evalue": "name 'null' is not defined",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mNameError\u001b[0m                                 Traceback (most recent call last)",
      "\u001b[1;32m<ipython-input-3-e22dced3bcf6>\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[1;32m----> 1\u001b[1;33m \u001b[1;32mfrom\u001b[0m \u001b[0mgenerate_pyrankvote_election_results\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mpyrankvote_main\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m      2\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mpandas\u001b[0m \u001b[1;32mas\u001b[0m \u001b[0mpd\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      3\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      4\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      5\u001b[0m \u001b[1;32mdef\u001b[0m \u001b[0mcreate_ballot_dict\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mballots\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\github\\ranked-choice-voting\\pyrankobjs\\generate_pyrankvote_election_results.py\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[0;32m    131\u001b[0m   {\n\u001b[0;32m    132\u001b[0m    \u001b[1;34m\"cell_type\"\u001b[0m\u001b[1;33m:\u001b[0m \u001b[1;34m\"code\"\u001b[0m\u001b[1;33m,\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 133\u001b[1;33m    \u001b[1;34m\"execution_count\"\u001b[0m\u001b[1;33m:\u001b[0m \u001b[0mnull\u001b[0m\u001b[1;33m,\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    134\u001b[0m    \u001b[1;34m\"metadata\"\u001b[0m\u001b[1;33m:\u001b[0m \u001b[1;33m{\u001b[0m\u001b[1;33m}\u001b[0m\u001b[1;33m,\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    135\u001b[0m    \u001b[1;34m\"outputs\"\u001b[0m\u001b[1;33m:\u001b[0m \u001b[1;33m[\u001b[0m\u001b[1;33m]\u001b[0m\u001b[1;33m,\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;31mNameError\u001b[0m: name 'null' is not defined"
     ]
    }
   ],
   "source": [
    "from generate_pyrankvote_election_results import pyrankvote_main\n",
    "import pandas as pd\n",
    "\n",
    "\n",
    "def create_ballot_dict(ballots):\n",
    "    \"\"\"\n",
    "    \"\"\"\n",
    "    all_ballots = ballots\n",
    "    ballot_dict = {}\n",
    "    for i in range(len(all_ballots)):\n",
    "        ballot_str = str(all_ballots[i])\n",
    "        curr_ballot = all_ballots[i]\n",
    "        if ballot_str in ballot_dict:\n",
    "            ballot_dict[ballot_str][0] = ballot_dict[ballot_str][0] + 1\n",
    "        else:\n",
    "            ballot_dict[ballot_str] = [1, all_ballots[i]]\n",
    "    return ballot_dict\n",
    "\n",
    "\n",
    "def create_candidate_matrix(candidates):\n",
    "    candidate_names = []\n",
    "    for cand in candidates:\n",
    "        candidate_names.append(cand.name)\n",
    "\n",
    "    cand_matrix = pd.DataFrame(0, columns=candidate_names, index=candidate_names)\n",
    "    return cand_matrix\n",
    "\n",
    "\n",
    "def symbolize_cand_matrix(cand_matrix):\n",
    "    for i in cand_matrix.index:\n",
    "        for j in cand_matrix.columns:\n",
    "            if i == j:\n",
    "                cand_matrix.loc[i, j] = '`'\n",
    "            else:\n",
    "                if cand_matrix.loc[i, j] != '++' and cand_matrix.loc[i, j] != '--':\n",
    "                    if cand_matrix.loc[i, j] > cand_matrix.loc[j, i]:\n",
    "                        cand_matrix.loc[i, j] = '++'\n",
    "                        cand_matrix.loc[j, i] = '--'\n",
    "                    else:\n",
    "                        cand_matrix.loc[i, j] = '--'\n",
    "                        cand_matrix.loc[j, i] = '++'\n",
    "    return cand_matrix\n",
    "\n",
    "\n",
    "def countX(lst, x):\n",
    "    return lst.count(x)\n",
    "\n",
    "\n",
    "def return_winners(cand_matrix):\n",
    "    results = []\n",
    "    result_dict = {}\n",
    "    for i in cand_matrix.index:\n",
    "        key = ''.join([str(countX(list(cand_matrix.loc[i]), '--') + 1), \". \", i])\n",
    "        result_dict[key] = [countX(list(cand_matrix.loc[i]), '--') + 1,\n",
    "                            (countX(list(cand_matrix.loc[i]), '++'), countX(list(cand_matrix.loc[i]), '--'))]\n",
    "    for key, item in sorted(result_dict.items(), key=lambda x: x[1]):\n",
    "        results.append(\"Rank %s: [Rank, (Wins, losses] %s\" % (key, item))\n",
    "\n",
    "    return results\n",
    "\n",
    "\n",
    "def condorcet_compile(candidates, ballots):\n",
    "    ballot_dict = create_ballot_dict(ballots)\n",
    "\n",
    "    candidate_names = []\n",
    "    for cand in candidates:\n",
    "        candidate_names.append(cand.name)\n",
    "\n",
    "    cand_matrix = pd.DataFrame(0, columns=candidate_names, index=candidate_names)\n",
    "\n",
    "    for votes, ballot in ballot_dict.values():\n",
    "        ranked_candidates = [cand.name for cand in list(ballot.ranked_candidates)]\n",
    "        process_cands = list(cand_matrix.columns)\n",
    "        for i, current_cand in enumerate(ranked_candidates):\n",
    "            process_cands.remove(current_cand)\n",
    "            cand_matrix.loc[current_cand][process_cands] = cand_matrix.loc[current_cand][process_cands] + votes\n",
    "\n",
    "    symbolize_cand_matrix(cand_matrix)\n",
    "    return return_winners(cand_matrix)\n",
    "\n",
    "\n",
    "def parse_condorcet_results(condorcet_results):  # list\n",
    "    parsed_results = []\n",
    "\n",
    "    for i in condorcet_results:\n",
    "        cand = i.split(':')[0].split('. ')[1]\n",
    "        wins = int(i.split(':')[1].split(', ')[-2:][0].split('(')[1])\n",
    "        parsed_results.append((cand, wins))\n",
    "\n",
    "    return parsed_results\n",
    "\n",
    "\n",
    "def return_condorcet_winner(parsed_results):\n",
    "    return sorted(parsed_results, key=lambda x: x[1], reverse=True)[0][0]\n",
    "\n",
    "def condorcet_main(file_path_of_election):\n",
    "    # candidates = list of Candidate() objects\n",
    "    # ballots = list of Ballot() objects\n",
    "    df, cand_list, ballots = pyrankvote_main(file_path_of_election)\n",
    "    condorcet_results = condorcet_compile(cand_list, ballots)\n",
    "    parsed_condorcet_results = parse_condorcet_results(condorcet_results)\n",
    "    winner = return_condorcet_winner(parsed_condorcet_results)\n",
    "\n",
    "    df['condorcet_winner'] = winner\n",
    "\n",
    "    if df['pyrankvote_winner'].all() != df['condorcet_winner'].all():\n",
    "        df['spoiled'] = 'Y'\n",
    "    else:\n",
    "        df['spoiled'] = 'N'\n",
    "    return df\n",
    "\n",
    "\n",
    "if __name__ == \"__main__\":  # # would read in concatenated csvs here\n",
    "    df = condorcet_main('../data/election_07-16-2020_11-08-11_3cands_0.0033333333333333335noise.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}

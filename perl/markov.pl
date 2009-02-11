#!/usr/bin/perl 
#
# Sentence generator using markov chain
#
# Usage:
#  1) Training mode
#    markov.pl -t -o chain.hdb < input.txt
#
#  2) Generation mode
#    markov.pl -g -n chain.hdb
#

use strict;
use warnings;
use Encode qw(decode encode);
use Getopt::Long;
use Text::MeCab;
use TokyoCabinet;
use Data::Dumper;

use constant {
    SEP           => "\t",
    NONWORD       => " ",
    SENTENCE_END  => "。",
    SAVE_INTERVAL => 10000,
    NUM_PREFIX    => 2,
};

sub usage_exit {
    print <<'USAGE';
Usage: 
 1) Training mode
  $ markov.pl -t -o dbm < input.txt
     -t, --train         training mode
     -o, --output dbm    output dbm path of word chain

 2) Generation mode
  $ markov.pl -g -n dbm
     -g, --generate      generation mode
     -c, --chain dbm     dbm path of word chain
USAGE
    exit 1;
}

sub _split_words {
    my ($mecab, $text) = @_;
    return if !$mecab || !$text;

    my @words;
    for (my $node = $mecab->parse($text); $node; $node = $node->next) {
        push @words, $node->surface if $node->surface;
    }
    return \@words;
}

sub _add_chain {
    my ($chain, $words) = @_;
    return if !$chain || !$words;

    my @prefixes;
    for (my $i = 0; $i < NUM_PREFIX; $i++) {
        push @prefixes, NONWORD;
    }
    my $nullkey = join SEP, (NONWORD) x NUM_PREFIX;
    foreach my $word (@{ $words }) {
        my $key = join SEP, @prefixes;
        next if $key eq $nullkey && $word eq SENTENCE_END;
        push @{ $chain->{$key} }, $word;
        shift @prefixes;
        push @prefixes, $word;
    }
}

sub _save_chain {
    my ($dbm, $chain) = @_;
    return if !$dbm || !$chain;

    foreach my $key (keys %{ $chain }) {
        my $words = $chain->{$key};
        next if !$words;
        my $val = join SEP, @{ $words };
        if ($dbm->get($key)) {
            $dbm->putcat($key, SEP.$val);
        }
        else {
            $dbm->putcat($key, $val);
        }
    }
}

sub train {
    my $dbpath = shift;
    return if !$dbpath;

    my $hdb = TokyoCabinet::HDB->new;
    if (!$hdb->open($dbpath, $hdb->OWRITER | $hdb->OCREAT | $hdb->OTRUNC)) {
        die "cannot open $dbpath";
    }

    my $mecab = Text::MeCab->new();
    my %chain;
    my $cnt = 0;
    while (my $line = <STDIN>) {
        my $words = _split_words($mecab, $line);
        _add_chain(\%chain, $words);
        if (++$cnt % SAVE_INTERVAL == 0) {
            _save_chain($hdb, \%chain);
            %chain = ();
        }
    }
}

sub generate {
    my $dbpath = shift;
    return if !$dbpath;

    my $hdb = TokyoCabinet::HDB->new;
    if (!$hdb->open($dbpath, $hdb->OREADER)) {
        die "cannot open $dbpath";
    }

    my @prefixes;
    for (my $i = 0; $i < NUM_PREFIX; $i++) {
        push @prefixes, NONWORD;
    }
    my $text;
    my $cnt = 0;
    while ($cnt < 5) {
        my $key = join SEP, @prefixes;
        my $val = $hdb->get($key);
        last if !$val;
        my @suffixes = split SEP, $val;
        my $suffix = $suffixes[rand @suffixes];
        last if !defined $suffix;
        $text .= $suffix;
        ++$cnt if $suffix eq SENTENCE_END;
        shift @prefixes;
        push @prefixes, $suffix;
    }
    print "$text\n";
}

sub main {
    my ($opt_train, $opt_gen, $opt_out, $opt_chain);
    GetOptions(
        'train'    => \$opt_train,
        'generate' => \$opt_gen,
        'output=s' => \$opt_out,
        'chain=s'  => \$opt_chain,
    );
    if ($opt_train && $opt_out) {
        train($opt_out);
    }
    elsif ($opt_gen && $opt_chain) {
        generate($opt_chain);
    }
    else {
        usage_exit();
    }
}

main();
